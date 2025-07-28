from contextlib import contextmanager
from typing import Generator

from cirq import MeasurementKey, OP_TREE, Operation, R, TaggedOperation

from stim_experiments.custom_dataclasses.configuration_error_correcing_code import ConfigurationErrorCorrectingCode
from stim_experiments.custom_dataclasses.logical_operation import LogicalGateLabel, LogicalOperation
from stim_experiments.custom_dataclasses.universal_operations_context import UniversalOperationsContext
from stim_experiments.error_correcting_codes.repetition_code.repetition_code import RepetitionCodeOneLogical
from stim_experiments.error_correcting_codes.support.controlled_single_qubit_gates_applier import \
    ControlledSingleQubitGatesApplier
from stim_experiments.error_correcting_codes.support.measurer.measurer import Measurer
from stim_experiments.error_correcting_codes.cat_parity_code.cat_parity_code import \
    CatParityCode
from stim_experiments.error_correcting_codes.support.multiple_cat_code.multiple_cat_code import MultipleCatCode
from stim_experiments.globals.active_encodings_store import ActiveEncodingsStore
from stim_experiments.globals.error_correcting_code_configuration import ConfigurationErrorCorrectingCodeManager
from stim_experiments.globals.fresh_ancillas_pool import FreshAncillasPool


class UniversalOperationsUtilities:
    def __init__(self, num_qubits_for_logical_operations: int):
        self._num_qubits_for_logical_operations = num_qubits_for_logical_operations

    def encode_multiple_cat(self, context: UniversalOperationsContext) -> OP_TREE:
        with ActiveEncodingsStore(additional_tracked_encodings=[context.multiple_cat_code]) as encodings_store:
            return [
                context.multiple_cat_code.encode_logical_qubit(),
                encodings_store.get_all_correction_circuits()
            ]

    def c_operations_helpers_to_data(self, operations: list[Operation], context: UniversalOperationsContext) -> list[OP_TREE]:
        repetition_codes = [RepetitionCodeOneLogical(num_qubits=len(subregister), qubits=subregister)
                            for subregister in context.cat_parity_code.subregisters]
        with ActiveEncodingsStore(additional_tracked_encodings=repetition_codes) as encodings_store:
            return [
                [
                    ControlledSingleQubitGatesApplier(operations=operations, controls=subregister[:len(operations)]).get_circuit(),
                    encodings_store.get_all_correction_circuits(),
                ]
                for subregister in context.multiple_cat_code.subregisters
            ]

    def measure_out_helper(self, measurement_key: MeasurementKey, context: UniversalOperationsContext) -> OP_TREE:
        logical_z = list(context.multiple_cat_code.get_operation_circuit(
            operation=LogicalOperation(gate=LogicalGateLabel.Z, qubit_index=0)
        ).all_operations())
        return self._measurer_type(observables=[logical_z], measurement_keys=[measurement_key]).get_measurement_circuit()

    @staticmethod
    def reset_ancilla_qubits(context: UniversalOperationsContext):
        return [TaggedOperation(R(qubit), f'RESET_HELPER_QUBITS_{context.__class__.__name__}')
                for qubit in context.ancilla_qubits]

    @contextmanager
    def use_fresh_ancilla_qubits(self) -> Generator[UniversalOperationsContext, None, None]:
        num_qubits_for_subregister_parity_code = self._num_qubits_for_logical_operations * self._num_cat_states
        with FreshAncillasPool().use_fresh_ancillas(num_ancillas=num_qubits_for_subregister_parity_code) as ancilla_qubits:
            multiple_cat_code = MultipleCatCode(num_cats=self._num_cat_states,
                                                num_qubits_per_cat=self._num_qubits_for_logical_operations,
                                                qubits=ancilla_qubits)
            cat_parity_code = CatParityCode(num_cats=self._num_cat_states,
                                            num_qubits_per_cat=self._num_qubits_for_logical_operations,
                                            qubits=ancilla_qubits)
            yield UniversalOperationsContext(
                ancilla_qubits=ancilla_qubits,
                cat_parity_code=cat_parity_code,
                multiple_cat_code=multiple_cat_code,
            )

    @property
    def _measurer_type(self) -> type[Measurer]:
        return self._configuration.measurer_type

    @property
    def _num_cat_states(self) -> int:
        return self._configuration.num_cat_states

    @property
    def _configuration(self) -> ConfigurationErrorCorrectingCode:
        return ConfigurationErrorCorrectingCodeManager().get_configuration()
