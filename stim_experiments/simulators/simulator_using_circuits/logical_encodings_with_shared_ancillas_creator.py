from abc import ABC, abstractmethod

from cirq import LineQubit
from numpy import ceil
from proto.utils import cached_property

from stim_experiments.error_correcting_codes.error_correcting_code.error_correcting_code import ErrorCorrectingCode
from stim_experiments.simulators.simulator_using_circuits.custom_dataclasses.logical_encodings_with_shared_ancillas import \
    LogicalEncodingsWithSharedAncillas


class LogicalEncodingsWithSharedAncillasCreator(ABC):
    @abstractmethod
    def create_encodings(self) -> LogicalEncodingsWithSharedAncillas:
        pass


class LogicalEncodingsWithSharedAncillasCreatorMultipleCodes(LogicalEncodingsWithSharedAncillasCreator):
    def __init__(self, error_correcting_codes: list[ErrorCorrectingCode]):
        self._error_correcting_codes = error_correcting_codes

    def create_encodings(self) -> LogicalEncodingsWithSharedAncillas:
        encodings = []
        current_index = 0
        for code in self._error_correcting_codes:
            new_code = code.create_new(
                qubit_start_index=current_index,
                provided_ancilla_qubits=self._shared_ancilla_qubits[:len(code.ancilla_qubits)]
            )
            encodings.append(new_code)
            current_index += len(new_code.data_qubits)
        return LogicalEncodingsWithSharedAncillas(
            encodings=encodings,
            ancillas=self._shared_ancilla_qubits
        )

    @cached_property
    def _shared_ancilla_qubits(self) -> list[LineQubit]:
        num_shared_ancilla_qubits = max(len(code.ancilla_qubits) for code in self._error_correcting_codes)
        start_index = sum(len(code.data_qubits) for code in self._error_correcting_codes)
        return LineQubit.range(start_index, start_index + num_shared_ancilla_qubits)


class LogicalEncodingsWithSharedAncillasCreatorSingleCode(LogicalEncodingsWithSharedAncillasCreator):
    def __init__(self, error_correcting_code: ErrorCorrectingCode, num_logical_qubits_needed: int = 1):
        self._error_correcting_code = error_correcting_code
        self._num_logical_qubits_needed = num_logical_qubits_needed

    def create_encodings(self) -> LogicalEncodingsWithSharedAncillas:
        encodings = [
            self._error_correcting_code.create_new(
                qubit_start_index=i * len(self._error_correcting_code.data_qubits),
                provided_ancilla_qubits=self._shared_ancilla_qubits
            )
            for i in range(self._num_encodings)
        ]
        return LogicalEncodingsWithSharedAncillas(
            encodings=encodings,
            ancillas=self._shared_ancilla_qubits
        )

    @cached_property
    def _shared_ancilla_qubits(self) -> list[LineQubit]:
        num_shared_ancilla_qubits = len(self._error_correcting_code.ancilla_qubits)
        start_index = len(self._error_correcting_code.data_qubits) * self._num_encodings
        return LineQubit.range(start_index, start_index + num_shared_ancilla_qubits)

    @cached_property
    def _num_encodings(self) -> int:
        qubits_per_code = self._error_correcting_code.num_logical_qubits
        return int(ceil(self._num_logical_qubits_needed / qubits_per_code))
