from abc import ABC, abstractmethod

from cirq import Circuit

from stim_experiments.error_correcting_codes.error_correcting_code.error_correcting_code import ErrorCorrectingCode


class UniversalHadamard(ABC):
    def __init__(self, code: ErrorCorrectingCode, qubit_index: int):
        self._code = code
        self._qubit_index = qubit_index

    @abstractmethod
    def get_hadamard_circuit(self) -> Circuit:
        pass
