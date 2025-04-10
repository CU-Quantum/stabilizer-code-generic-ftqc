from typing import re

import pytest
from numpy import array

from stim_experiments.error_correcting_codes.generic_stabilizer_code.custom_dataclasses.check_matrix import CheckMatrix, \
    TYPE_CHECK_MATRIX
from tests.error_correcting_codes.generic_stabilizer_code.utilities import CHECK_MATRIX_STEANE_VALUES


ARBITRARY_CHECK_MATRIX = array([[1, 1]])


class TestStabilizersStandardizer:
    def test_must_have_even_number_of_columns(self):
        with pytest.raises(ValueError, match="Check matrix must have have an even number of columns."):
            CheckMatrix(matrix=array([[1]]))

    def test_check_matrix_is_accessible(self):
        check_matrix = CheckMatrix(matrix=CHECK_MATRIX_STEANE_VALUES)
        assert check_matrix.matrix.tolist() == CHECK_MATRIX_STEANE_VALUES.tolist()

    @pytest.mark.parametrize(['matrix', 'expected_num_qubits'], [(CHECK_MATRIX_STEANE_VALUES, 7), (ARBITRARY_CHECK_MATRIX, 1)])
    def test_determines_num_physical_qubits(self, matrix: TYPE_CHECK_MATRIX, expected_num_qubits: int):
        check_matrix = CheckMatrix(matrix=matrix)
        num_physical_qubits = check_matrix.num_physical_qubits
        assert num_physical_qubits == expected_num_qubits

    def test_num_logical_qubits_is_settable(self):
        check_matrix_default = CheckMatrix(matrix=ARBITRARY_CHECK_MATRIX)
        assert check_matrix_default.num_logical_qubits == 1

        check_matrix = CheckMatrix(matrix=ARBITRARY_CHECK_MATRIX, num_logical_qubits=2)
        assert check_matrix.num_logical_qubits == 2

    def test_determines_rank_of_pauli_x_portion(self):
        check_matrix = CheckMatrix(matrix=CHECK_MATRIX_STEANE_VALUES)
        rank = check_matrix.rank_of_pauli_x_portion
        assert rank == 3

    def test_there_are_n_minus_k_rows(self):
        different_number_of_logical_qubits_than_expected = 2
        with pytest.raises(ValueError, match="Check matrix must have n-k rows."):
            CheckMatrix(matrix=CHECK_MATRIX_STEANE_VALUES, num_logical_qubits=different_number_of_logical_qubits_than_expected)

    def test_can_set_qubit_order(self):
        num_physical_qubits = 7
        matrix_default = CheckMatrix(matrix=CHECK_MATRIX_STEANE_VALUES)
        assert matrix_default.qubit_order == list(range(num_physical_qubits))

        set_qubit_order = [1,0,2,3,4,5,6]
        matrix_default = CheckMatrix(matrix=CHECK_MATRIX_STEANE_VALUES, qubit_order=set_qubit_order)
        assert matrix_default.qubit_order == set_qubit_order

    def test_cannot_set_incorrect_number_of_qubits(self):
        with pytest.raises(ValueError, match=re.escape("Qubit order must be a permutation of the number of qubits.")):
            CheckMatrix(matrix=CHECK_MATRIX_STEANE_VALUES, qubit_order=[0,1,2,3,4,5,7])

    def test_qubit_order_changes_after_swapping_qubits(self):
        matrix = CheckMatrix(matrix=CHECK_MATRIX_STEANE_VALUES, qubit_order=[0,1,2,3,4,5,6])
        matrix.swap_qubits(column_indices=(0, 1))
        assert matrix.qubit_order == [1,0,2,3,4,5,6]

    def test_columns_are_swapped_after_swapping_qubits_in_pauli_x(self):
        matrix = CheckMatrix(matrix=CHECK_MATRIX_STEANE_VALUES, qubit_order=[0,1,2,3,4,5,6])
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
        matrix = CheckMatrix(matrix=CHECK_MATRIX_STEANE_VALUES, qubit_order=[0,1,2,3,4,5,6])
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
        matrix = CheckMatrix(matrix=CHECK_MATRIX_STEANE_VALUES)
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
