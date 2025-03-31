from abc import ABC

from numpy import array
from numpy._typing import NDArray


class ErrorCorrectingCode(ABC):
    def __init__(self):
        self._current_state = array([])

    def get_current_state(self) -> NDArray[NDArray[complex]]:
        return self._current_state
