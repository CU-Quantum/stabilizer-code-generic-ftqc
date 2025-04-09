from dataclasses import dataclass

from numpy import array
from numpy._typing import NDArray
from numpy.ma.core import allequal



class CheckMatrixStandardizer:
    def __init__(self, check_matrix: NDArray[NDArray[bool]], num_logical_qubits: int = 1):
        self._check_matrix = check_matrix
        self._num_logical_qubits = num_logical_qubits

    def get_standardized_matrix(self) -> NDArray[NDArray[bool]]:
        return self._check_matrix


class TestCheckMatrixStandardizer:
    def test_empty(self):
        standardizer = CheckMatrixStandardizer(check_matrix=array([[]]))
        standardized_check = standardizer.get_standardized_matrix()
        assert allequal(standardized_check, array([[]]))

    def test_one(self):
        standardizer = CheckMatrixStandardizer(check_matrix=array([[1, 1]]))
        standardized_check = standardizer.get_standardized_matrix()
        assert allequal(standardized_check, array([[1, 1]]))

    def test_steane(self):
        check_matrix_steane = array([
            [0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0],
            [0, 1, 1, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0],
            [1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1],
            [0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 1, 1],
            [0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 1],
        ])
        assert False
