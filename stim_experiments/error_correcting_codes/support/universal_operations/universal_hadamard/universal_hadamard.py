from abc import ABC, abstractmethod

from cirq import Circuit

from stim_experiments.custom_dataclasses.simulation_operation import LogicalEncodingIndex
from stim_experiments.error_correcting_codes.error_correcting_code.error_correcting_code import ErrorCorrectingCode


class UniversalHadamard(ABC):
    def __init__(self, code: LogicalEncodingIndex):
        self._code = code.encoding
        self._qubit_index = code.qubit_index_relative

    @abstractmethod
    def get_hadamard_circuit(self) -> Circuit:
        pass
