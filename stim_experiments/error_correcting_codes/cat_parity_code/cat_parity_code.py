from typing import Optional

from cirq import Circuit, LineQubit, Operation, X, Z
from numpy import array

from stim_experiments.custom_dataclasses.logical_operation import LogicalGateLabel, LogicalOperation
from stim_experiments.custom_dataclasses.check_matrix import CheckMatrix
from stim_experiments.error_correcting_codes.stabilizer_code.stabilizer_code import StabilizerCode
from stim_experiments.error_correcting_codes.support.check_matrix_to_operations import CheckMatrixToOperations
from stim_experiments.error_correcting_codes.support.error_recovery.error_recovery_by_syndrome_and_recoveries import \
    ErrorRecoveryByStabilizers
from stim_experiments.error_correcting_codes.support.multiple_cat_code_generators import \
    MultipleCatCodeGenerators
from stim_experiments.error_correcting_codes.support.recovery_combinations_finder import RecoveryCombinationsFinder
from stim_experiments.error_correcting_codes.support.recovery_finder import RecoveryFinder


class CatParityCode(StabilizerCode):
    def __init__(self, num_cats: int, num_qubits_per_cat: int, qubits: Optional[list[LineQubit]] = None):
        self._num_cats = num_cats
        self._num_qubits_per_cat = num_qubits_per_cat

        generator = MultipleCatCodeGenerators(num_qubits_per_cat=self._num_qubits_per_cat,
                                              num_cats=self._num_cats)
        z_stabilizers = generator.get_z_generators()
        x_stabilizers = generator.get_x_generators()

        self._check_matrix = CheckMatrix(matrix=array(z_stabilizers + x_stabilizers))
        super().__init__(check_matrix=self._check_matrix,
                         recovery_combinations_finder=RecoveryCombinationsFinder(max_num_x_errors=self._num_qubits_per_cat // 2,
                                                                                 max_num_z_errors=self._num_cats // 2),
                         qubits=qubits)

    def _get_anticommuter_for_generator(self, generator_index: int) -> list[Operation]:
        x_stabilizer_start_index = self._num_generators - self._num_cats + 1
        is_z_stabilizer = generator_index < x_stabilizer_start_index
        if is_z_stabilizer:
            num_checks_per_register = self._num_qubits_per_cat - 1
            subregister_index = generator_index // num_checks_per_register
            start_index = subregister_index * self._num_qubits_per_cat
            relative_generator_index = generator_index % num_checks_per_register
            return [X(self.data_qubits[qubit_index]) for qubit_index in range(start_index, start_index + relative_generator_index + 1)]
        else:
            is_last_generator = generator_index == self._num_generators - 1
            if is_last_generator:
                return [Z(self.data_qubits[-1])]
            subregister_index = generator_index - x_stabilizer_start_index
            return [Z(self.data_qubits[i * self._num_qubits_per_cat]) for i in range(subregister_index + 1)]

    def _perform_get_operation_circuit(self, operation: LogicalOperation) -> Optional[Circuit]:
        if operation.gate == LogicalGateLabel.X:
            return Circuit(
                [X(self.data_qubits[i]) for i in range(self._num_qubits_per_cat)]
            )
        elif operation.gate == LogicalGateLabel.Z:
            return Circuit(
                [Z(self.data_qubits[i * self._num_qubits_per_cat]) for i in range(self._num_cats)],
            )
        return None

    def get_modified_x_stabilizers_error_correction_circuit(self,
                                                            subregister_control_index: int,
                                                            target_operations: list[Operation]) -> Circuit: # TODO make this correct both x and z errors
        last_subregister_index = len(self.subregisters) - 1
        x_matrix = CheckMatrix(matrix=self._check_matrix.matrix[-last_subregister_index:])
        x_stabilizers_modified = CheckMatrixToOperations(check_matrix=x_matrix, qubits=self.data_qubits).get_operations()
        if subregister_control_index < last_subregister_index:
            x_stabilizers_modified[subregister_control_index] += target_operations
        recoveries = RecoveryFinder(check_matrix=x_matrix).find_recovery_operations(qubits=self._qubits)
        return ErrorRecoveryByStabilizers(
            stabilizers=x_stabilizers_modified,
            recoveries=recoveries,
        ).get_error_correction_circuit()

    @property
    def subregisters(self) -> list[list[LineQubit]]:
        return [self.data_qubits[i * self._num_qubits_per_cat:(i + 1) * self._num_qubits_per_cat]
                for i in range(self._num_cats)]

    @property
    def _num_generators(self) -> int:
        return len(self._check_matrix.matrix)
