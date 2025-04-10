import re

import pytest
from numpy import array

from stim_experiments.error_correcting_codes.generic_stabilizer_code.custom_dataclasses.check_matrix_standardized import \
    CheckMatrixStandardized


class TestStabilizersStandardizer:
    @pytest.fixture(autouse=True)
    def _setup(self):
        self._valid_standardized_check_matrix = array([
            [1, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0],
            [0, 1, 0, 1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 1, 0, 0, 1],
            [0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 1, 0, 1],
            [0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 1, 0],
        ])

    def test_identity_in_pauli_x_portion(self):
        matrix_without_correct_identity_in_pauli_x_portion = self._valid_standardized_check_matrix
        matrix_without_correct_identity_in_pauli_x_portion[:2, :2] = [[0, 1], [1, 0]]
        with pytest.raises(ValueError, match=re.escape("The first (r)x(r) submatrix must be the identity.")):
            CheckMatrixStandardized(matrix=matrix_without_correct_identity_in_pauli_x_portion)

    def test_zeros_in_pauli_x_portion(self):
        rank_of_pauli_x_portion = 3

        matrix_with_ones_in_pauli_x_portion_below_rank = self._valid_standardized_check_matrix
        matrix_with_ones_in_pauli_x_portion_below_rank[rank_of_pauli_x_portion] = matrix_with_ones_in_pauli_x_portion_below_rank[0]
        with pytest.raises(ValueError, match="All rows in the pauli_x portion below the rank must be 0."):
            CheckMatrixStandardized(matrix=matrix_with_ones_in_pauli_x_portion_below_rank)

    def test_zeros_in_pauli_z_portion(self):
        num_logical_qubits = 1
        matrix_with_ones_in_c_one_submatrix = self._valid_standardized_check_matrix
        matrix_with_ones_in_c_one_submatrix[0, -num_logical_qubits - 1] = 1
        with pytest.raises(ValueError, match=re.escape("The (r)x(n-k-r) submatrix beginning at index [0, n+r] must be 0.")):
            CheckMatrixStandardized(matrix=matrix_with_ones_in_c_one_submatrix)

    def test_identity_in_pauli_z_portion(self):
        num_logical_qubits = 1
        rank_of_pauli_x_portion = 3

        matrix_without_correct_identity_in_pauli_z_portion = self._valid_standardized_check_matrix
        matrix_without_correct_identity_in_pauli_z_portion[rank_of_pauli_x_portion + 1, -num_logical_qubits - 1] = 1
        with pytest.raises(ValueError, match=re.escape("The (n-k-r)x(n-k-r) submatrix beginning at index [r, n+r] must be the identity.")):
            CheckMatrixStandardized(matrix=matrix_without_correct_identity_in_pauli_z_portion)

    def test_can_retrieve_a1_submatrix(self):
        matrix = CheckMatrixStandardized(matrix=self._valid_standardized_check_matrix)
        submatrix = matrix.a1_submatrix
        assert submatrix.tolist() == [[0, 1, 1], [1, 0, 1], [1, 1, 1]]

    def test_can_retrieve_a2_submatrix(self):
        matrix = CheckMatrixStandardized(matrix=self._valid_standardized_check_matrix)
        submatrix = matrix.a2_submatrix
        assert submatrix.tolist(), [[1], [1], [0]]

    def test_can_retrieve_b_submatrix(self):
        matrix = CheckMatrixStandardized(matrix=self._valid_standardized_check_matrix)
        submatrix = matrix.b_submatrix
        assert submatrix.tolist() == [[0, 0, 0], [0, 0, 0], [0, 0, 0]]

    def test_can_retrieve_c_submatrix(self):
        matrix = CheckMatrixStandardized(matrix=self._valid_standardized_check_matrix)
        submatrix = matrix.c_submatrix
        assert submatrix.tolist() == [[0], [0], [0]]

    def test_can_retrieve_d_submatrix(self):
        matrix = CheckMatrixStandardized(matrix=self._valid_standardized_check_matrix)
        submatrix = matrix.d_submatrix
        assert submatrix.tolist() == [[1, 0, 1], [0, 1, 1], [1, 1, 1]]

    def test_can_retrieve_e_submatrix(self):
        matrix = CheckMatrixStandardized(matrix=self._valid_standardized_check_matrix)
        submatrix = matrix.e_submatrix
        assert submatrix.tolist() == [[1], [1], [0]]
