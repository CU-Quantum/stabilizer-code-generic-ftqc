from contextlib import contextmanager
from dataclasses import asdict
from functools import cached_property
from typing import Generator
from uuid import uuid4

from cirq import Circuit, CircuitOperation, FrozenCircuit, Moment, OP_TREE, Operation, TaggedOperation

from stim_experiments.custom_dataclasses.configuration_error_correcing_code import ConfigurationErrorCorrectingCode
from stim_experiments.custom_dataclasses.logical_operation import LogicalGateLabel, LogicalOperation
from stim_experiments.custom_dataclasses.simulation_operation import LogicalEncodingIndex
from stim_experiments.custom_dataclasses.universal_controlled_operation_fault_tolerant_context import \
    UniversalControlledOperationFaultTolerantContext
from stim_experiments.error_correcting_codes.support.measurer.measurer import Measurer
from stim_experiments.error_correcting_codes.support.universal_operations.universal_controlled_flip.universal_controlled_flip import \
    UniversalControlledOperation
from stim_experiments.error_correcting_codes.support.universal_operations.universal_hadamard.universal_hadamard import \
    UniversalHadamard
from stim_experiments.error_correcting_codes.support.universal_operations.universal_operations_utilities import \
    UniversalOperationsUtilities
from stim_experiments.globals.error_correcting_code_configuration import ConfigurationErrorCorrectingCodeManager
from stim_experiments.utilities.measurement_key_with_stable_hash import MeasurementKeyWithStableHash


UNIVERSAL_CONTROLLED_FLIP_CZ_TAG = 'UNIVERSAL_CONTROLLED_FLIP_CZ'
UNIVERSAL_CONTROLLED_FLIP_C_TAG = 'UNIVERSAL_CONTROLLED_FLIP_C'


class UniversalControlledFlipFaultTolerant(UniversalControlledOperation):
    def get_controlled_operation_circuit(self) -> Circuit:
        with self._use_fresh_ancilla_qubits() as context:
            return Circuit(
                Moment(self._reset_ancilla_qubits(context=context)),
                self._encode_three_cat(context=context),
                self._cz_helpers_to_control(context=context),
                self._universal_hadamard_type(code=LogicalEncodingIndex(encoding=context.multiple_cat_code, qubit_index_relative=0)).get_hadamard_circuit(),
                self._c_helpers_to_target(context=context),
                self._measure_out_helper(context=context),
            )

    def _encode_three_cat(self, context: UniversalControlledOperationFaultTolerantContext) -> OP_TREE:
        return self._universal_operations_utilities.encode_multiple_cat(context=context)

    def _cz_helpers_to_control(self, context: UniversalControlledOperationFaultTolerantContext) -> OP_TREE:
        return [
            TaggedOperation(
                CircuitOperation(
                    FrozenCircuit(
                        self._universal_operations_utilities.c_operations_helpers_to_data(
                            operations=context.data_code_logical_z,
                            context=context
                        )
                    )
                ),
                UNIVERSAL_CONTROLLED_FLIP_CZ_TAG
            ),
        ]

    def _c_helpers_to_target(self, context: UniversalControlledOperationFaultTolerantContext) -> OP_TREE:
        return TaggedOperation(
            CircuitOperation(
                FrozenCircuit(
                    self._universal_operations_utilities.c_operations_helpers_to_data(
                        operations=context.target_operations,
                        context=context
                    )
                )
            ),
            UNIVERSAL_CONTROLLED_FLIP_C_TAG
        )

    def _measure_out_helper(self, context: UniversalControlledOperationFaultTolerantContext) -> OP_TREE:
        measurement_key = MeasurementKeyWithStableHash(f'UNIVERSAL_CONTROLLED_OPERATION_MEASUREMENT_{uuid4().hex}')
        return FrozenCircuit(  # cirq seems to be reversing the order of these operations when not frozen
            self._universal_operations_utilities.measure_out_helper(measurement_key=measurement_key, context=context),
            CircuitOperation(FrozenCircuit(context.data_code_logical_z)).with_classical_controls(measurement_key),
        )

    def _reset_ancilla_qubits(self, context: UniversalControlledOperationFaultTolerantContext):
        return self._universal_operations_utilities.reset_ancilla_qubits(context=context)

    @contextmanager
    def _use_fresh_ancilla_qubits(self) -> Generator[UniversalControlledOperationFaultTolerantContext, None, None]:
        with self._universal_operations_utilities.use_fresh_ancilla_qubits() as base_context:
            yield UniversalControlledOperationFaultTolerantContext(
                **asdict(base_context),
                data_code_logical_x=self._get_control_logical_operations(gate_label=LogicalGateLabel.X),
                data_code_logical_z=self._get_control_logical_operations(gate_label=LogicalGateLabel.Z),
                target_operations=list(self._target.encoding.get_operation_circuit(self._target.operation).all_operations()),
            )

    @cached_property
    def _universal_operations_utilities(self) -> UniversalOperationsUtilities:
        control_logical_z = list(self._control.encoding.get_operation_circuit(
            operation=LogicalOperation(gate=LogicalGateLabel.Z, qubit_index=self._control.qubit_index_relative)
        ).all_operations())
        target_logical_operations = list(self._target.encoding.get_operation_circuit(self._target.operation).all_operations())
        num_qubits_for_logical_operations = max(len(control_logical_z), len(target_logical_operations))
        return UniversalOperationsUtilities(num_qubits_for_logical_operations=num_qubits_for_logical_operations)

    def _get_control_logical_operations(self, gate_label: LogicalGateLabel) -> list[Operation]:
        return list(self._control.encoding.get_operation_circuit(
            operation=LogicalOperation(gate=gate_label, qubit_index=self._control.qubit_index_relative)
        ).all_operations())

    @property
    def _universal_hadamard_type(self) -> type[UniversalHadamard]:
        return self._configuration.universal_hadamard_type

    @property
    def _measurer_type(self) -> type[Measurer]:
        return self._configuration.measurer_type

    @property
    def _configuration(self) -> ConfigurationErrorCorrectingCode:
        return ConfigurationErrorCorrectingCodeManager().get_configuration()
