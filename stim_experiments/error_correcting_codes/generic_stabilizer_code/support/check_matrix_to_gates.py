from typing import List

from cirq import Gate, X, Z

from stim_experiments.error_correcting_codes.generic_stabilizer_code.custom_dataclasses.check_matrix import CheckMatrix


class CheckMatrixToGates:
    def __init__(self, check_matrix: CheckMatrix) -> None:
        self._check_matrix = check_matrix

    def get_gates(self) -> List[List[List[Gate]]]:
        return [[self._get_operations(row=row, qubit_index=qubit_index) for qubit_index in range(self._check_matrix.num_physical_qubits)]
                for row in self._check_matrix.matrix]

    def _get_operations(self, row: List[bool], qubit_index: int) -> List[Gate]:
        operations = []
        if row[qubit_index]:
            operations.append(X)
        if row[qubit_index + self._check_matrix.num_physical_qubits]:
            operations.append(Z)
        return operations
