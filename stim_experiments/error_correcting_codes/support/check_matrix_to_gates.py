from typing import List

from cirq import Gate, LineQubit, Operation, X, Z

from stim_experiments.custom_dataclasses.check_matrix import CheckMatrix


class CheckMatrixToGates:
    def __init__(self, check_matrix: CheckMatrix) -> None:
        self._check_matrix = check_matrix

    def get_gates(self) -> List[List[List[Gate]]]:
        return [[self._get_operations(row=row, qubit_index=qubit_index) for qubit_index in range(self._check_matrix.num_physical_qubits)]
                for row in self._check_matrix.matrix]

    def _get_operations(self, row: List[bool], qubit_index: int) -> List[Gate]:
        operations = []
        if row[qubit_index]:
            is_negative = row[qubit_index] == -1
            if is_negative:
                operations.append(Z)
            operations.append(X)
            if is_negative:
                operations.append(Z)
        if row[qubit_index + self._check_matrix.num_physical_qubits]:
            is_negative = row[qubit_index + self._check_matrix.num_physical_qubits] == -1
            if is_negative:
                operations.append(X)
            operations.append(Z)
            if is_negative:
                operations.append(X)
        return operations


class CheckMatrixToOperations:
    def __init__(self, check_matrix: CheckMatrix, qubits: list[LineQubit]):
        self._check_matrix = check_matrix
        self._qubits = qubits

    def get_operations(self) -> list[list[Operation]]:
        generator_gates = CheckMatrixToGates(check_matrix=self._check_matrix).get_gates()
        return [[gate(self._qubits[target_index])
                 for target_index, gates in enumerate(qubit_gates)
                 for gate in gates]
                for qubit_gates in generator_gates]
