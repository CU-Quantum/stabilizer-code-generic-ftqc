from abc import ABC, abstractmethod


class ErrorCorrectingCode(ABC):
    @abstractmethod
    def circuit_string(self) -> str:
        pass

    @property
    @abstractmethod
    def data_coordinates(self):
        pass
