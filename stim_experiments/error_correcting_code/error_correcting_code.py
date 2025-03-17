from abc import ABC, abstractmethod
from typing import List, Tuple


class ErrorCorrectingCode(ABC):
    @abstractmethod
    def circuit_string(self) -> str:
        pass

    @property
    @abstractmethod
    def data_coordinates(self) -> List[Tuple[float, float]]:
        pass
