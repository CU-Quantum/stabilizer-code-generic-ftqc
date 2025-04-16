from dataclasses import dataclass
from typing import Dict, List

from numpy._typing import NDArray

from stim_experiments.error_correcting_codes.error_correcting_code.error_correcting_code import ErrorCorrectingCode


@dataclass
class SimulatorResult:
    encodings: List[ErrorCorrectingCode]
    measurements: Dict[str, NDArray[bool]]

    def __eq__(self, other):
        keys = zip(self.measurements, other.measurements)
        values = zip(self.measurements.values(), other.measurements.values())
        return (self.encodings == other.encodings
                and all(key == other_key for key, other_key in keys)
                and all(value == other_value for value, other_value in values))
