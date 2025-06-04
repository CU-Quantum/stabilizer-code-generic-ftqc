from contextlib import contextmanager
from dataclasses import asdict
from functools import cached_property
from typing import Generator
from uuid import uuid4

from cirq import Circuit, CircuitOperation, FrozenCircuit, MeasurementKey, OP_TREE, Operation, Z
from numpy import array

from stim_experiments.conditions.recovery_condition import RecoveryCondition
from stim_experiments.custom_dataclasses.check_matrix import CheckMatrix
from stim_experiments.custom_dataclasses.configuration_error_correcing_code import ConfigurationErrorCorrectingCode
from stim_experiments.custom_dataclasses.logical_operation import LogicalGateLabel, LogicalOperation
from stim_experiments.custom_dataclasses.recovery import RecoveryOperations
from stim_experiments.custom_dataclasses.simulation_operation import LogicalEncodingIndex
from stim_experiments.custom_dataclasses.universal_controlled_operation_fault_tolerant_context import \
    UniversalControlledOperationFaultTolerantContext
from stim_experiments.error_correcting_codes.support.check_matrix_to_operations import CheckMatrixToOperations
from stim_experiments.error_correcting_codes.support.measurer.measurer import Measurer
from stim_experiments.error_correcting_codes.support.universal_operations.universal_controlled_operation.universal_controlled_operation import \
    UniversalControlledOperation
from stim_experiments.error_correcting_codes.support.universal_operations.universal_hadamard.universal_hadamard import \
    UniversalHadamard
from stim_experiments.error_correcting_codes.support.universal_operations.universal_operations_utilities import \
    UniversalOperationsUtilities
from stim_experiments.globals.active_encodings_store import ActiveEncodingsStore
from stim_experiments.globals.error_correcting_code_configuration import ConfigurationErrorCorrectingCodeManager


class UniversalControlledOperationFaultTolerant(UniversalControlledOperation):
    def get_controlled_operation_circuit(self) -> Circuit:
        with self._use_fresh_ancilla_qubits() as context:
            return Circuit(
                self._encode_three_cat(context=context),
                self._cz_helpers_to_control(context=context),
                self._ensure_subregister_parity_in_plus(context=context),
                self._universal_hadamard_type(code=LogicalEncodingIndex(encoding=context.three_cat, qubit_index_relative=0)).get_hadamard_circuit(),
                self._c_helpers_to_target(context=context),
                self._measure_out_helper(context=context),
                self._reset_ancilla_qubits(context=context),
            )

    def _encode_three_cat(self, context: UniversalControlledOperationFaultTolerantContext) -> OP_TREE:
        return self._universal_operations_utilities.encode_three_cat(context=context)

    def _cz_helpers_to_control(self, context: UniversalControlledOperationFaultTolerantContext) -> OP_TREE:
        return self._universal_operations_utilities.c_operations_helpers_to_data(
            operations=context.data_code_logical_z,
            context=context
        )

    def _ensure_subregister_parity_in_plus(self, context: UniversalControlledOperationFaultTolerantContext) -> OP_TREE:
        cat_parity_x = list(context.cat_parity_code.get_operation_circuit(
            operation=LogicalOperation(gate=LogicalGateLabel.X, qubit_index=0)
        ).all_operations())
        return self._universal_operations_utilities.ensure_cat_parity_code_in_plus(
            observable=cat_parity_x + context.data_code_logical_z,
            context=context
        )

    def _c_helpers_to_target(self, context: UniversalControlledOperationFaultTolerantContext) -> OP_TREE:
        subregister_operations = self._universal_operations_utilities.c_operations_helpers_to_data(
            operations=context.target_operations,
            context=context
        )

        num_qubits_per_cat_state = len(context.cat_parity_code.subregisters[0])
        z_matrix = CheckMatrix(matrix=array(
            [
                [1] * 2 * num_qubits_per_cat_state + [0] * (num_qubits_per_cat_state + len(context.cat_parity_code.data_qubits)),
                [0] * num_qubits_per_cat_state + [1] * 2 * num_qubits_per_cat_state + [0] * len(context.cat_parity_code.data_qubits)
            ]
        ))

        for i, subregister_operation in enumerate(subregister_operations):
            measurement_key = MeasurementKey(f'MODIFIED_Z_STABILIZERS_{i}_{uuid4()}')
            z_stabilizers_modified = CheckMatrixToOperations(check_matrix=z_matrix,
                                                             qubits=context.cat_parity_code.data_qubits).get_operations()
            if i < 2:
                z_stabilizers_modified[i] += context.target_operations

            syndrome_operations = [
                self._measurer_type(
                    operations=operations,
                    measurement_key=measurement_key,
                ).get_measurement_circuit()
                for operations in z_stabilizers_modified
            ]
            recoveries = [
                RecoveryOperations(
                    operation=Z(subregister[0]),
                    symptom=[int(i < 2), int(i > 0)]
                )
                for i, subregister in enumerate(context.cat_parity_code.subregisters)
            ]
            recovery_operations = [
                recovery.operation.with_classical_controls(
                    RecoveryCondition(key=measurement_key, symptom=recovery.symptom))
                for recovery in recoveries
            ]

            subregister_operations[i] += [syndrome_operations, recovery_operations]

        return subregister_operations

    def _measure_out_helper(self, context: UniversalControlledOperationFaultTolerantContext) -> OP_TREE:
        measurement_key = MeasurementKey(f'UNIVERSAL_CONTROLLED_OPERATION_MEASUREMENT_{uuid4().hex}')
        with ActiveEncodingsStore(additional_tracked_encodings=[]) as encodings_store:
            return [
                FrozenCircuit(  # cirq seems to be reversing the order of these operations when not frozen
                    self._universal_operations_utilities.measure_out_helper(measurement_key=measurement_key, context=context),
                    encodings_store.get_all_correction_circuits(),
                    CircuitOperation(FrozenCircuit(context.data_code_logical_z)).with_classical_controls(measurement_key),
                ),
                encodings_store.get_all_correction_circuits(),
            ]

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
