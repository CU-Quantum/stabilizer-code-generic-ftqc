from abc import ABC

from numpy import array
from numpy._typing import NDArray

from stim_experiments.utilities import DENSITY_MATRIX_TYPE


class ErrorCorrectingCode(ABC):
    def __init__(self, initial_qubit_state_density_matrix: DENSITY_MATRIX_TYPE):
        self._initial_qubit_state_density_matrix = initial_qubit_state_density_matrix
        self._current_state = array([])

    def get_current_state(self) -> NDArray[NDArray[complex]]:
        return self._current_state
