from abc import ABC, abstractmethod

from cirq import Circuit

from cirq_experiments.custom_dataclasses.simulation_operation import LogicalEncodingIndex


class UniversalHadamard(ABC):
    def __init__(self, code: LogicalEncodingIndex):
        self._code = code.encoding
        self._qubit_index = code.qubit_index_relative

    @abstractmethod
    def get_hadamard_circuit(self) -> Circuit:
        pass
