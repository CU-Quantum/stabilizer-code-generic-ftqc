from abc import ABC, abstractmethod
from typing import Optional

from cirq import Circuit, MeasurementKey, Operation


class Measurer(ABC):
    def __init__(self,
                 operations: list[Operation],
                 measurement_key: Optional[MeasurementKey] = None,
                 ):
        self._operations = operations
        self._measurement_key = measurement_key

    @abstractmethod
    def get_measurement_circuit(self) -> Circuit:
        pass
