from collections import defaultdict
from dataclasses import dataclass, field

from stim_experiments.utilities import TYPE_STATE_VECTOR_OR_DENSITY_MATRIX
from tests.utilities import states_are_equal


@dataclass
class StateAndMeasurements:
    state: TYPE_STATE_VECTOR_OR_DENSITY_MATRIX
    measurements: dict[int, list[int]] = field(default_factory=lambda: defaultdict(list))

    def __eq__(self, other):
        return states_are_equal(self.state, other.state) and self.measurements == other.measurements
