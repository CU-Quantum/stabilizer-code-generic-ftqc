from abc import ABC, abstractmethod
from typing import Dict, Iterable, List, Tuple

from stim_experiments.surface_code.coursera_custom.support.utilities import index_string


class ErrorCorrectingCode(ABC):
    def __init__(self):
        self.circuit_string = ""

    def apply_logical_hadamard(self) -> str:
        return f"""

        H {self._data_indices_str}
        DEPOLARIZE1 {self._data_indices_str}

        """

    @property
    def _data_indices_str(self) -> str:
        return index_string(self.data_coordinates, self.coordinates_to_index_map)

    @abstractmethod
    def surface_code_string(self) -> str:
        pass

    @property
    @abstractmethod
    def data_coordinates(self) -> List[Tuple[float, float]]:
        pass

    @property
    @abstractmethod
    def coordinates_to_index_map(self) -> Dict[Iterable[float], int]:
        pass
