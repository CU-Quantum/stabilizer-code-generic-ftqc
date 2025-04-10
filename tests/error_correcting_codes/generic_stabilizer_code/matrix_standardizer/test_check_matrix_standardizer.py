from numpy import array
from numpy.ma.core import allequal

from stim_experiments.error_correcting_codes.generic_stabilizer_code.custom_dataclasses.check_matrix import CheckMatrix
from stim_experiments.error_correcting_codes.generic_stabilizer_code.custom_dataclasses.check_matrix_standardized import \
    CheckMatrixStandardized
from stim_experiments.error_correcting_codes.generic_stabilizer_code.matrix_standardizer.check_matrix_standardizer import \
    CheckMatrixStandardizer
from tests.error_correcting_codes.generic_stabilizer_code.utilities import get_check_matrix_values_steane


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
        standardizer = CheckMatrixStandardizer(check_matrix=CheckMatrix(matrix=get_check_matrix_values_steane()))
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
