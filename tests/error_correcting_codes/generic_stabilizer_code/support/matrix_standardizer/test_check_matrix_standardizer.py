import copy
from re import escape

import pytest
from numpy import array
from numpy.ma.core import allequal

from stim_experiments.error_correcting_codes.generic_stabilizer_code.custom_dataclasses.check_matrix import CheckMatrix
from stim_experiments.error_correcting_codes.generic_stabilizer_code.custom_dataclasses.check_matrix_standardized import \
    CheckMatrixStandardized
from stim_experiments.error_correcting_codes.generic_stabilizer_code.support.matrix_standardizer.check_matrix_standardizer import \
    CheckMatrixStandardizer
from tests.error_correcting_codes.generic_stabilizer_code.utilities import get_check_matrix_values_4_qubit, \
    get_check_matrix_values_4_qubit_standardized, get_check_matrix_values_steane, \
    get_check_matrix_values_steane_standardized


class TestCheckMatrixStandardizer:
    def test_empty(self):
        with pytest.raises(ValueError, match=escape("The number of rows must be less than half the number of columns. Shape (1, 0) was provided.")):
            CheckMatrixStandardizer(check_matrix=CheckMatrix(matrix=array([[]])))

    def test_one(self):
        standardizer = CheckMatrixStandardizer(check_matrix=CheckMatrix(matrix=array([[1, 1]])))
        standardized_check = standardizer.get_standardized_matrix()
        assert allequal(standardized_check, CheckMatrix(matrix=array([[1, 1]])))

    def test_steane(self):
        standardizer = CheckMatrixStandardizer(check_matrix=CheckMatrix(matrix=get_check_matrix_values_steane()))
        standardized_check = standardizer.get_standardized_matrix()
        assert standardized_check == CheckMatrixStandardized(
            matrix=get_check_matrix_values_steane_standardized(),
            qubit_order=[0,1,3,2,4,6,5],
        )

    def test_4_qubit(self):
        standardizer = CheckMatrixStandardizer(check_matrix=CheckMatrix(matrix=get_check_matrix_values_4_qubit()))
        standardized_check = standardizer.get_standardized_matrix()
        assert standardized_check == CheckMatrixStandardized(
            matrix=get_check_matrix_values_4_qubit_standardized(),
            qubit_order=[0, 1, 2, 3],
        )

    def test_does_not_modify_original_check_matrix(self):
        generators = get_check_matrix_values_4_qubit()
        original_check_matrix = CheckMatrix(matrix=copy.deepcopy(generators))
        CheckMatrixStandardizer(check_matrix=original_check_matrix).get_standardized_matrix()
        assert original_check_matrix.matrix.tolist() == generators.tolist()
