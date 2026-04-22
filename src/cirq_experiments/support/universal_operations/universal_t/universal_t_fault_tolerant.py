from contextlib import contextmanager
from dataclasses import dataclass
from typing import Generator
from uuid import uuid4

from cirq import Circuit, CircuitOperation, LineQubit, FrozenCircuit, Moment, OP_TREE, R, TaggedOperation
import sympy

from cirq_experiments.custom_dataclasses.configuration_error_correcing_code import ConfigurationErrorCorrectingCode
from cirq_experiments.custom_dataclasses.logical_operation import LogicalGateLabel, LogicalOperation
from cirq_experiments.custom_dataclasses.simulation_operation import LogicalEncodingIndex
from cirq_experiments.support.universal_operations.universal_hadamard.universal_hadamard import UniversalHadamard
from cirq_experiments.support.measurer.measurer import Measurer
from cirq_experiments.support.operations_applier.operations_applier import DELAYED_NOISE_TAG
from cirq_experiments.support.universal_operations.universal_t.universal_t import UniversalT
from cirq_experiments.error_correcting_codes.tetrahedral_code.tetrahedral_code import TetrahedralCode
from cirq_experiments.globals.active_encodings_store import ActiveEncodingsStore
from cirq_experiments.globals.error_correcting_code_configuration import ConfigurationErrorCorrectingCodeManager
from cirq_experiments.globals.fresh_ancillas_pool import FreshAncillasPool
from cirq_experiments.utilities.measurement_key_with_stable_hash import MeasurementKeyWithStableHash


UNIVERSAL_T_MEASUREMENT_TAG = 'UNIVERSAL_T_MEASUREMENT_TAG'


@dataclass
class UniversalTFaultTolerantContext:
    ancilla_qubits: list[LineQubit]
    tetrahedral: TetrahedralCode


class UniversalTFaultTolerant(UniversalT):
    def get_t_circuit(self) -> Circuit:
        with self._use_fresh_ancilla_qubits() as context:
            return Circuit(
                Moment(self._reset_ancilla_qubits(context=context)),
                self._encode_tetrahedral(context=context),
                self._cx_code_to_tetrahedral(context=context),
                self._perform_t_on_tetrahedral(context=context),
                self._measure_out_helper(context=context),
            )

    def _encode_tetrahedral(self, context: UniversalTFaultTolerantContext) -> OP_TREE:
        with ActiveEncodingsStore(additional_tracked_encodings=[context.tetrahedral]) as encodings_store:
            return [
                context.tetrahedral.encode_logical_qubit(),
                encodings_store.get_all_correction_circuits(),
            ]

    def _cx_code_to_tetrahedral(self, context: UniversalTFaultTolerantContext) -> OP_TREE:
        zz_measurement_key = MeasurementKeyWithStableHash(f'UNIVERSAL_T_ZZ_MEASUREMENT_{uuid4().hex}')
        control_logical_z = list(self._encoding.encoding.get_operation_circuit(
            operation=LogicalOperation(gate=LogicalGateLabel.Z, qubit_index=self._encoding.qubit_index_relative)
        ).all_operations())
        target_logical_z = list(context.tetrahedral.get_operation_circuit(
            operation=LogicalOperation(gate=LogicalGateLabel.Z, qubit_index=0)
        ).all_operations())
        target_logical_x = list(context.tetrahedral.get_operation_circuit(
            operation=LogicalOperation(gate=LogicalGateLabel.X, qubit_index=0)
        ).all_operations())
        with ActiveEncodingsStore(additional_tracked_encodings=[context.tetrahedral]) as encodings_store:
            return [
                self._universal_hadamard_type(
                    code=LogicalEncodingIndex(encoding=context.tetrahedral, qubit_index_relative=0)
                ).get_hadamard_circuit(),
                encodings_store.get_all_correction_circuits(),
                self._measurer_type(
                    observables=[control_logical_z + target_logical_z],
                    measurement_keys=[zz_measurement_key],
                ).get_measurement_circuit(),
                encodings_store.get_all_correction_circuits(),
                CircuitOperation(
                    FrozenCircuit(target_logical_x)
                ).with_classical_controls(zz_measurement_key),
                encodings_store.get_all_correction_circuits(),
            ]

    def _perform_t_on_tetrahedral(self, context: UniversalTFaultTolerantContext) -> OP_TREE:
        with ActiveEncodingsStore(additional_tracked_encodings=[context.tetrahedral]) as encodings_store:
            return [
                context.tetrahedral.get_operation_circuit(LogicalOperation(gate=LogicalGateLabel.T, qubit_index=0)),
                encodings_store.get_all_correction_circuits(),
            ]

    def _measure_out_helper(self, context: UniversalTFaultTolerantContext) -> OP_TREE:
        measurement_key = MeasurementKeyWithStableHash(f'UNIVERSAL_T_MEASUREMENT_{uuid4().hex}')
        measurement_key_symbol = sympy.symbols(measurement_key.name)
        helper_code_logical_x = list(context.tetrahedral.get_operation_circuit(
            operation=LogicalOperation(gate=LogicalGateLabel.X, qubit_index=0)
        ).all_operations())
        data_code_logical_z = list(self._encoding.encoding.get_operation_circuit(
            operation=LogicalOperation(gate=LogicalGateLabel.Z, qubit_index=self._encoding.qubit_index_relative)
        ).all_operations())
        with ActiveEncodingsStore(additional_tracked_encodings=[]) as encodings_store:
            return TaggedOperation(
                CircuitOperation(
                    FrozenCircuit(
                        self._measurer_type(observables=[helper_code_logical_x], measurement_keys=[measurement_key]).get_measurement_circuit(),
                        encodings_store.get_all_correction_circuits(),
                        FrozenCircuit(TaggedOperation(  # FrozenCircuit to keep separate from correction round
                            CircuitOperation(
                                FrozenCircuit(
                                    CircuitOperation(
                                        FrozenCircuit(data_code_logical_z)).with_classical_controls(
                                        measurement_key),
                                )
                            ),
                            DELAYED_NOISE_TAG
                        )),
                    )
                ),
                UNIVERSAL_T_MEASUREMENT_TAG
            )

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
    def _universal_hadamard_type(self) -> type[UniversalHadamard]:
        return self._configuration.universal_hadamard_type

    @property
    def _measurer_type(self) -> type[Measurer]:
        return self._configuration.measurer_type

    @property
    def _configuration(self) -> ConfigurationErrorCorrectingCode:
        return ConfigurationErrorCorrectingCodeManager().get_configuration()
