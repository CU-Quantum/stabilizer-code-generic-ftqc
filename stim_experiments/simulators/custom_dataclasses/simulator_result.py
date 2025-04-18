from dataclasses import dataclass
from typing import Dict

from numpy._typing import NDArray
from numpy.ma import allequal

from stim_experiments.utilities import TYPE_STATE_VECTOR_OR_DENSITY_MATRIX


@dataclass
class SimulatorResult:
    current_state: TYPE_STATE_VECTOR_OR_DENSITY_MATRIX
    measurements: Dict[str, NDArray[bool]]

    def __eq__(self, other):
        keys = zip(self.measurements, other.measurements)
        values = zip(self.measurements.values(), other.measurements.values())
        return (allequal(self.current_state, other.current_state)
                and all(key == other_key for key, other_key in keys)
                and all(value == other_value for value, other_value in values))
