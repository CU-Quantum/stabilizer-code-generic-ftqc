from typing import Optional
from uuid import uuid4

from cirq import Circuit, LineQubit, MeasurementKey, Operation, X, Z
from numpy import array

from stim_experiments.conditions.recovery_condition import RecoveryCondition
from stim_experiments.custom_dataclasses.logical_operation import LogicalGateLabel, LogicalOperation
from stim_experiments.custom_dataclasses.check_matrix import CheckMatrix
from stim_experiments.custom_dataclasses.recovery import RecoveryOperations
from stim_experiments.error_correcting_codes.stabilizer_code.stabilizer_code import StabilizerCode
from stim_experiments.error_correcting_codes.support.check_matrix_to_operations import CheckMatrixToOperations
from stim_experiments.error_correcting_codes.support.error_recovery.error_recovery_by_syndrome_and_recoveries import \
    ErrorRecoveryByStabilizers
from stim_experiments.error_correcting_codes.support.measurer.measurer import Measurer
from stim_experiments.error_correcting_codes.three_cat_code.three_cat_code import ThreeCatCode
from stim_experiments.globals.error_correcting_code_configuration import ConfigurationErrorCorrectingCodeManager
from stim_experiments.utilities.repetition_z_stabilizers_multicat_generator import \
    RepetitionZStabilizersMulticatGenerator


class CatParityCode(StabilizerCode):
    num_cats = ThreeCatCode.num_cats

    def __init__(self, num_qubits_in_cat_state: int, qubits: Optional[list[LineQubit]] = None):
        self._num_qubits_in_cat_state = num_qubits_in_cat_state
        num_data_qubits = num_qubits_in_cat_state * self.num_cats

        z_stabilizers = RepetitionZStabilizersMulticatGenerator(num_qubits_in_cat=self._num_qubits_in_cat_state, num_cats=self.num_cats).get_stabilizers()
        x_stabilizers = [
            [int(cat_index * self._num_qubits_in_cat_state <= qubit_index < (cat_index + 2) * self._num_qubits_in_cat_state)
             for qubit_index in range(num_data_qubits)] + [0] * num_data_qubits
            for cat_index in range(self.num_cats - 1)
        ]

        self._check_matrix = CheckMatrix(matrix=array(z_stabilizers + x_stabilizers))
        super().__init__(check_matrix=self._check_matrix, qubits=qubits)

    def _get_anticommuter_for_generator(self, generator_index: int) -> list[Operation]:
        is_z_stabilizer = generator_index < self._num_generators - 2
        if is_z_stabilizer:
            num_checks_per_register = self._num_qubits_in_cat_state - 1
            register_index = generator_index // num_checks_per_register
            start_index = register_index * self._num_qubits_in_cat_state
            relative_generator_index = generator_index % num_checks_per_register
            return [X(self.data_qubits[qubit_index]) for qubit_index in range(start_index, start_index + relative_generator_index + 1)]
        else:
            is_last_generator = generator_index == self._num_generators - 1
            return [Z(self.data_qubits[0 - is_last_generator])]

    def _perform_get_operation_circuit(self, operation: LogicalOperation) -> Optional[Circuit]:
        if operation.gate == LogicalGateLabel.X:
            return Circuit(
                [X(self.data_qubits[i]) for i in range(self._num_qubits_in_cat_state)]
            )
        elif operation.gate == LogicalGateLabel.Z:
            return Circuit(
                [Z(self.data_qubits[i * self._num_qubits_in_cat_state]) for i in range(self.num_cats)],
            )
        return None

    def get_modified_x_stabilizers_error_correction_circuit(self,
                                                            subregister_control_index: int,
                                                            target_operations: list[Operation]) -> Circuit:
        x_matrix = CheckMatrix(matrix=self._check_matrix.matrix[-2:])
        x_stabilizers_modified = CheckMatrixToOperations(check_matrix=x_matrix, qubits=self.data_qubits).get_operations()
        if subregister_control_index < 2:
            x_stabilizers_modified[subregister_control_index] += target_operations
        recoveries = [
            RecoveryOperations(
                operation=Z(subregister[0]),
                symptom=[int(i < 2), int(i > 0)]
            )
            for i, subregister in enumerate(self.subregisters)
        ]
        return ErrorRecoveryByStabilizers(
            stabilizers=x_stabilizers_modified,
            recoveries=recoveries,
        ).get_error_correction_circuit()

    @property
    def subregisters(self) -> list[list[LineQubit]]:
        return [self.data_qubits[i * self._num_qubits_in_cat_state:(i + 1) * self._num_qubits_in_cat_state]
                for i in range(self.num_cats)]

    @property
    def _num_generators(self) -> int:
        return len(self._check_matrix.matrix)
