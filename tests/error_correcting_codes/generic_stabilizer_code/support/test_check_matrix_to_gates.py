from typing import List

from cirq import Gate, X, Z
from numpy import array

from stim_experiments.error_correcting_codes.generic_stabilizer_code.custom_dataclasses.check_matrix import \
    CheckMatrix
from tests.error_correcting_codes.generic_stabilizer_code.utilities import get_check_matrix_values_4_qubit


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


class TestCheckMatrixToGates:
    def test_trivial(self):
        converter = CheckMatrixToGates(check_matrix=CheckMatrix(matrix=array([[]])))
        gates = converter.get_gates()
        assert gates == [[]]

    def test_x_gate(self):
        converter = CheckMatrixToGates(check_matrix=CheckMatrix(matrix=array([[1, 0]])))
        gates = converter.get_gates()
        assert gates == [[[X]]]

    def test_z_gate(self):
        converter = CheckMatrixToGates(check_matrix=CheckMatrix(matrix=array([[0, 1]])))
        gates = converter.get_gates()
        assert gates == [[[Z]]]

    def test_y_gate(self):
        converter = CheckMatrixToGates(check_matrix=CheckMatrix(matrix=array([[1, 1]])))
        gates = converter.get_gates()
        assert gates == [[[X, Z]]]

    def test_4_qubit(self):
        check_matrix = CheckMatrix(matrix=get_check_matrix_values_4_qubit())
        converter = CheckMatrixToGates(check_matrix=check_matrix)
        gates = converter.get_gates()
        assert gates == [
            [[X], [Z], [Z], [X]],
            [[X, Z], [X], [X], [X, Z]],
        ]
