from re import escape

import pytest
from numpy import array

from stim_experiments.error_correcting_codes.generic_stabilizer_code.custom_dataclasses.check_matrix import CheckMatrix, \
    TYPE_CHECK_MATRIX
from tests.error_correcting_codes.generic_stabilizer_code.utilities import get_check_matrix_values_steane


def get_arbitrary_check_matrix_values():
    return array([[1, 1]])


class TestStabilizersStandardizer:
    @pytest.fixture(autouse=True)
    def _setup(self):
        self._steane_matrix_values = get_check_matrix_values_steane()

    def test_must_have_even_number_of_columns(self):
        with pytest.raises(ValueError, match=escape("Check matrix must have have an even number of columns. Shape (1, 3) was provided.")):
            CheckMatrix(matrix=array([[1, 1, 1]]))

    def test_check_matrix_is_accessible(self):
        check_matrix = CheckMatrix(matrix=self._steane_matrix_values)
        assert check_matrix.matrix.tolist() == self._steane_matrix_values.tolist()

    @pytest.mark.parametrize(['matrix', 'expected_num_qubits'], [(get_check_matrix_values_steane(), 7), (get_arbitrary_check_matrix_values(), 1)])
    def test_determines_num_physical_qubits_is_half_num_columns(self, matrix: TYPE_CHECK_MATRIX, expected_num_qubits: int):
        check_matrix = CheckMatrix(matrix=matrix)
        num_qubits = check_matrix.num_physical_qubits
        assert num_qubits == expected_num_qubits

    @pytest.mark.parametrize(['matrix', 'expected_num_qubits'], [(get_check_matrix_values_steane(), 1), (array([[1, 1, 1, 1, 1, 1]]), 2)])
    def test_determines_num_logical_qubits_is_half_num_columns_minus_num_rows(self, matrix: TYPE_CHECK_MATRIX, expected_num_qubits: int):
        check_matrix = CheckMatrix(matrix=matrix)
        num_qubits = check_matrix.num_logical_qubits
        assert num_qubits == expected_num_qubits

    def test_determines_rank_of_pauli_x_portion(self):
        check_matrix = CheckMatrix(matrix=self._steane_matrix_values)
        rank = check_matrix.rank_of_pauli_x_portion
        assert rank == 3

    def test_can_set_qubit_order(self):
        num_physical_qubits = 7
        matrix_default = CheckMatrix(matrix=self._steane_matrix_values)
        assert matrix_default.qubit_order == list(range(num_physical_qubits))

        set_qubit_order = [1,0,2,3,4,5,6]
        matrix_default = CheckMatrix(matrix=self._steane_matrix_values, qubit_order=set_qubit_order)
        assert matrix_default.qubit_order == set_qubit_order

    def test_cannot_set_incorrect_number_of_qubits(self):
        with pytest.raises(ValueError, match=escape("Qubit order must be a permutation of the number of qubits. Order [0, 1, 2, 3, 4, 5, 7] was provided.")):
            CheckMatrix(matrix=self._steane_matrix_values, qubit_order=[0,1,2,3,4,5,7])

    def test_qubit_order_changes_after_swapping_qubits(self):
        matrix = CheckMatrix(matrix=self._steane_matrix_values, qubit_order=[0,1,2,3,4,5,6])
        matrix.swap_qubits(column_indices=(0, 1))
        assert matrix.qubit_order == [1,0,2,3,4,5,6]

    def test_columns_are_swapped_after_swapping_qubits_in_pauli_x(self):
        matrix = CheckMatrix(matrix=self._steane_matrix_values, qubit_order=[0,1,2,3,4,5,6])
        matrix.swap_qubits(column_indices=(0, 1))
        first_and_second_columns_in_both_pauli_x_and_z_are_switched =[
            [0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0],
            [1, 0, 1, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0],
            [0, 1, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1],
            [0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 1, 1],
            [0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 1, 0, 1],
        ]
        assert matrix.matrix.tolist() == first_and_second_columns_in_both_pauli_x_and_z_are_switched

    def test_columns_are_swapped_after_swapping_qubits_in_pauli_z(self):
        matrix = CheckMatrix(matrix=self._steane_matrix_values, qubit_order=[0,1,2,3,4,5,6])
        matrix.swap_qubits(column_indices=(7, 8))
        first_and_second_columns_in_both_pauli_x_and_z_are_switched =[
            [0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0],
            [1, 0, 1, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0],
            [0, 1, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1],
            [0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 1, 1],
            [0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 1, 0, 1],
        ]
        assert matrix.matrix.tolist() == first_and_second_columns_in_both_pauli_x_and_z_are_switched

    def test_add_rows(self):
        matrix = CheckMatrix(matrix=self._steane_matrix_values)
        matrix.add_rows(row_index=1, target_row_index=0)
        second_row_is_added_to_first = [
            [0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 1, 1, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0],
            [1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1],
            [0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 1, 1],
            [0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 1],
        ]
        assert matrix.matrix.tolist() == second_row_is_added_to_first
