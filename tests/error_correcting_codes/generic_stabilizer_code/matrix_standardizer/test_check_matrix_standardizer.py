from numpy import array
from numpy.ma.core import allequal

from stim_experiments.error_correcting_codes.generic_stabilizer_code.custom_dataclasses.check_matrix import CheckMatrix
from stim_experiments.error_correcting_codes.generic_stabilizer_code.custom_dataclasses.check_matrix_standardized import \
    CheckMatrixStandardized
from stim_experiments.error_correcting_codes.generic_stabilizer_code.matrix_standardizer.support.next_column_index_with_one_at_position_finder import \
    NextColumnIndexWithOneAtPositionFinder
from stim_experiments.error_correcting_codes.generic_stabilizer_code.matrix_standardizer.support.next_row_index_with_one_at_position_finder import \
    NextRowIndexWithOneAtPositionFinder
from tests.error_correcting_codes.generic_stabilizer_code.utilities import CHECK_MATRIX_STEANE_VALUES


class CheckMatrixStandardizer:
    def __init__(self, check_matrix: CheckMatrix, num_logical_qubits: int = 1):
        self._check_matrix = check_matrix
        self._num_logical_qubits = num_logical_qubits

        self._new_check_matrix = CheckMatrix(matrix=self._check_matrix.matrix)

    def get_standardized_matrix(self) -> CheckMatrixStandardized:
        self._set_first_identity_matrix()
        return CheckMatrixStandardized(
            matrix=self._new_check_matrix.matrix,
            qubit_order=self._new_check_matrix.qubit_order,
        )

    def _set_first_identity_matrix(self):
        for i in range(self._check_matrix.rank_of_pauli_x_portion):
            if not self._check_matrix.matrix[i, i]:
                row_index_with_one_in_column = NextRowIndexWithOneAtPositionFinder(matrix=self._new_check_matrix.matrix,
                                                                                   row_index=i,
                                                                                   column_index=i).get_row_index()
                if row_index_with_one_in_column is not None:
                    self._new_check_matrix.add_rows(row_index=row_index_with_one_in_column, target_row_index=i)
                else:
                    column_index_with_one_in_row = NextColumnIndexWithOneAtPositionFinder(matrix=self._new_check_matrix.matrix,
                                                                                          row_index=i,
                                                                                          column_index=i).get_column_index()
                    self._new_check_matrix.swap_qubits(column_indices=(i, column_index_with_one_in_row))



class TestCheckMatrixStandardizer:
    def test_empty(self):
        standardizer = CheckMatrixStandardizer(check_matrix=CheckMatrix(matrix=array([[]])))
        standardized_check = standardizer.get_standardized_matrix()
        assert allequal(standardized_check, array([[]]))

    def test_one(self):
        standardizer = CheckMatrixStandardizer(check_matrix=CheckMatrix(matrix=array([[1, 1]])))
        standardized_check = standardizer.get_standardized_matrix()
        assert allequal(standardized_check, array([[1, 1]]))

    def test_steane(self):
        standardizer = CheckMatrixStandardizer(check_matrix=CheckMatrix(matrix=CHECK_MATRIX_STEANE_VALUES))
        standardized_check = standardizer.get_standardized_matrix()
        assert standardized_check == CheckMatrixStandardized(
            matrix=array([
                [1, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 1, 0, 1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 1, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 1, 0, 0, 1],
                [0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 1, 0, 1],
                [0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 1, 0],
            ]),
            qubit_order=[0,1,3,2,4,6,5],
        )
