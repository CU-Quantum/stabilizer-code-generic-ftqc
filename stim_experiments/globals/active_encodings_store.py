from uuid import uuid4

from cirq import Circuit

from stim_experiments.error_correcting_codes.error_correcting_code.error_correcting_code import ErrorCorrectingCode


class ActiveEncodingsStore:
    _tracked_encodings: dict[str, list[ErrorCorrectingCode]] = {}

    def __init__(self, additional_tracked_encodings: list[ErrorCorrectingCode]):
        self._id = uuid4().hex
        self._tracked_encodings[self._id] = additional_tracked_encodings

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        del self._tracked_encodings[self._id]

    def get_all_correction_circuits(self) -> Circuit:
        return Circuit(
            encoding.get_error_correction_circuit()
            for encodings in self._tracked_encodings.values()
            for encoding in encodings
        )
