from abc import ABC, abstractmethod

from cirq import Circuit

from stim_experiments.custom_dataclasses.simulation_operation import LogicalEncodingIndex


class UniversalT(ABC):
    def __init__(self, code: LogicalEncodingIndex):
        self._encoding = code

    @abstractmethod
    def get_t_circuit(self) -> Circuit:
        pass
