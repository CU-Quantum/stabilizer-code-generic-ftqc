from collections import defaultdict
from dataclasses import dataclass, field

from numpy._typing import NDArray
from numpy.ma.core import allequal

from stim_experiments.utilities.utilities import TYPE_STATE_VECTOR_OR_DENSITY_MATRIX
from tests.utilities import states_are_equal


@dataclass
class StateAndMeasurements:
    state: TYPE_STATE_VECTOR_OR_DENSITY_MATRIX
    measurements: dict[str, NDArray[int]] = field(default_factory=lambda: defaultdict(list))

    def __eq__(self, other):
        return states_are_equal(self.state, other.state) \
            and list(self.measurements.keys()) == list(other.measurements.keys()) \
            and all(allequal(v, other.measurements[k]) for k, v in self.measurements.items())
