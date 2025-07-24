from abc import ABC, abstractmethod
from typing import Optional

from cirq import Circuit, MeasurementKey, Operation


class Measurer(ABC):
    def __init__(self,
                 observables: list[list[Operation]],
                 measurement_keys: Optional[list[MeasurementKey]] = None,
                 ):
        self._observables = observables
        self._measurement_keys = measurement_keys or []

    @abstractmethod
    def get_measurement_circuit(self) -> Circuit:
        pass
