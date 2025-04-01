from abc import ABC
from typing import List, Optional

from numpy import array, log2
from numpy._typing import NDArray

from stim_experiments.utilities import DENSITY_MATRIX_TYPE, partial_trace


class ErrorCorrectingCode(ABC):
    def __init__(self, initial_qubit_state_density_matrix: DENSITY_MATRIX_TYPE):
        self._initial_qubit_state_density_matrix = initial_qubit_state_density_matrix
        self._current_state = array([])

    def get_current_state(self, qubit_indices: Optional[List[int]] = None) -> NDArray[NDArray[complex]]:
        keep_qubits = qubit_indices or list(range(log2(self._current_state.shape[0])))
        return partial_trace(rho=self._current_state, keep_qubits=keep_qubits)
