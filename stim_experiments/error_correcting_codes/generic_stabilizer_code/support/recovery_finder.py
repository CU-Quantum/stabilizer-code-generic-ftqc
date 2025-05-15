from typing import List

from cirq import X, Y, Z

from stim_experiments.error_correcting_codes.custom_dataclasses.recovery import RecoveryGates
from stim_experiments.error_correcting_codes.generic_stabilizer_code.custom_dataclasses.check_matrix import CheckMatrix


class RecoveryFinder:
    def __init__(self, check_matrix: CheckMatrix):
        self._check_matrix = check_matrix

    def find_recoveries(self) -> List[RecoveryGates]:
        possible_errors = [X, Z]
        transposed_check_matrix = self._check_matrix.matrix.transpose()
        x_or_z_recoveries = [RecoveryGates(gate=possible_errors[column_index < self._check_matrix.num_physical_qubits],
                                           qubit_index=column_index % self._check_matrix.num_physical_qubits,
                                           symptom=syndrome.tolist())
                             for column_index, syndrome in enumerate(transposed_check_matrix)]
        y_recoveries = [RecoveryGates(gate=Y,
                                      qubit_index=column_index,
                                      symptom=self._get_y_symptom(column_index=column_index))
                        for column_index in range(self._check_matrix.num_physical_qubits)]
        return [recovery for recovery in x_or_z_recoveries + y_recoveries if any(recovery.symptom)]

    def _get_y_symptom(self, column_index: int) -> list[int]:
        transposed_check_matrix = self._check_matrix.matrix.transpose()
        reciprocal_column = column_index + self._check_matrix.num_physical_qubits
        return (transposed_check_matrix[column_index] ^ transposed_check_matrix[reciprocal_column]).tolist()
