from dataclasses import dataclass
from typing import Dict, List

from numpy import allclose
from numpy._typing import NDArray

from stim_experiments.utilities import TYPE_DENSITY_MATRIX


@dataclass
class SimulatorResult:
    state: List[TYPE_DENSITY_MATRIX]
    measurements: Dict[str, NDArray[bool]]

    def __eq__(self, other):
        keys = zip(self.measurements, other.measurements)
        values = zip(self.measurements.values(), other.measurements.values())
        return (all(allclose(qubit_state, other_state, atol=1e-7) for qubit_state, other_state in zip(self.state, other.state))
                and all(key == other_key for key, other_key in keys)
                and all(value == other_value for value, other_value in values))
