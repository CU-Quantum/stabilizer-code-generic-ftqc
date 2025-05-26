from contextlib import contextmanager
from dataclasses import dataclass
from functools import cached_property
from typing import Generator

from cirq import Circuit, LineQubit, OP_TREE, R

from stim_experiments.custom_dataclasses.logical_operation import LogicalGateLabel, LogicalOperation
from stim_experiments.custom_dataclasses.simulation_operation import TargetEncoding
from stim_experiments.error_correcting_codes.support.universal_operations.universal_controlled_operation.universal_controlled_operation import \
    UniversalControlledOperation
from stim_experiments.error_correcting_codes.support.universal_operations.universal_operations_utilities import \
    UniversalOperationsUtilities
from stim_experiments.error_correcting_codes.support.universal_operations.universal_t.universal_t import UniversalT
from stim_experiments.error_correcting_codes.tetrahedral_code.tetrahedral_code import TetrahedralCode
from stim_experiments.globals.active_encodings_store import ActiveEncodingsStore
from stim_experiments.globals.error_correcting_code_configuration import ConfigurationErrorCorrectingCodeManager
from stim_experiments.globals.fresh_ancillas_pool import FreshAncillasPool
from stim_experiments.utilities.universal_controlled_operation_type_factory import \
    UniversalControlledOperationTypeFactory


@dataclass
class UniversalTFaultTolerantContext:
    ancilla_qubits: list[LineQubit]
    tetrahedral: TetrahedralCode


class UniversalTFaultTolerant(UniversalT):
    def get_t_circuit(self) -> Circuit:
        with self._use_fresh_ancilla_qubits() as context:
            return Circuit(
                self._encode_tetrahedral(context=context),
                self._cx_code_to_tetrahedral(context=context),
                self._perform_t_on_tetrahedral(context=context),
                self._cx_code_to_tetrahedral(context=context),
                self._reset_ancilla_qubits(context=context),
            )

    def _encode_tetrahedral(self, context: UniversalTFaultTolerantContext) -> OP_TREE:
        with ActiveEncodingsStore(additional_tracked_encodings=[context.tetrahedral]) as encodings_store:
            return [
                context.tetrahedral.encode_logical_qubit(),
                encodings_store.get_all_correction_circuits(),
            ]

    def _cx_code_to_tetrahedral(self, context: UniversalTFaultTolerantContext) -> OP_TREE:
        target_encoding = TargetEncoding(operation=LogicalOperation(gate=LogicalGateLabel.X, qubit_index=0),
                                         encoding=context.tetrahedral)
        with ActiveEncodingsStore(additional_tracked_encodings=[context.tetrahedral]) as encodings_store:
            return [
                self._universal_controlled_operation_type(control=self._encoding, target=target_encoding).get_controlled_operation_circuit(),
                encodings_store.get_all_correction_circuits(),
            ]

    def _perform_t_on_tetrahedral(self, context: UniversalTFaultTolerantContext) -> OP_TREE:
        with ActiveEncodingsStore(additional_tracked_encodings=[context.tetrahedral]) as encodings_store:
            return [
                context.tetrahedral.get_operation_circuit(LogicalOperation(gate=LogicalGateLabel.T, qubit_index=0)),
                encodings_store.get_all_correction_circuits(),
            ]

    def _reset_ancilla_qubits(self, context: UniversalTFaultTolerantContext) -> OP_TREE:
        return [R(qubit) for qubit in context.ancilla_qubits]

    @contextmanager
    def _use_fresh_ancilla_qubits(self) -> Generator[UniversalTFaultTolerantContext, None, None]:
        tetrahedral_code = TetrahedralCode()
        with FreshAncillasPool().use_fresh_ancillas(num_ancillas=len(tetrahedral_code.data_qubits)) as ancilla_qubits:
            yield UniversalTFaultTolerantContext(
                ancilla_qubits=ancilla_qubits,
                tetrahedral=tetrahedral_code.create_new(qubits=ancilla_qubits),
            )

    @property
    def _universal_controlled_operation_type(self) -> type[UniversalControlledOperation]:
        controlled_operation_type = ConfigurationErrorCorrectingCodeManager().get_configuration().universal_controlled_operation_type
        return UniversalControlledOperationTypeFactory(controlled_operation_type=controlled_operation_type).get_universal_controlled_operation_type()
