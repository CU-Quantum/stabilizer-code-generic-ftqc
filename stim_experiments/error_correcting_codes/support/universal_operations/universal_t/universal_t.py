from abc import ABC, abstractmethod

from cirq import Circuit

from stim_experiments.custom_dataclasses.simulation_operation import LogicalEncodingIndex


class UniversalT(ABC):
    def __init__(self, code: LogicalEncodingIndex):
        self._code = code.encoding
        self._qubit_index = code.qubit_index_relative

    @abstractmethod
    def get_t_circuit(self) -> Circuit:
        pass
