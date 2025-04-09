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
