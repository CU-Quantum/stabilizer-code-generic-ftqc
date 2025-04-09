from numpy import array

from stim_experiments.error_correcting_codes.generic_stabilizer_code.custom_dataclasses.check_matrix_standardized import \
    CheckMatrixStandardized


class TestStabilizersStandardizer:
    def test_must_have_even_number_of_columns(self):
        assert False

    def test_check_matrix_is_accessible(self):
        steane_matrix_standardized = array([
            [1, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0],
            [0, 1, 0, 1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 1, 0, 0, 1],
            [0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 1, 0, 1],
            [0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 1, 0],
        ])
        check_matrix = CheckMatrixStandardized(matrix=steane_matrix_standardized)
        assert check_matrix.matrix.tolist() == steane_matrix_standardized.tolist()

    def test_check_matrix_is_accessible(self):
        steane_matrix_standardized = array([
            [1, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0],
            [0, 1, 0, 1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 1, 0, 0, 1],
            [0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 1, 0, 1],
            [0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 1, 0],
        ])
        check_matrix = CheckMatrixStandardized(matrix=steane_matrix_standardized)
        assert check_matrix.matrix.tolist() == steane_matrix_standardized.tolist()
