from collections import defaultdict
from dataclasses import dataclass, field

from numpy.ma import allclose

from stim_experiments.utilities import TYPE_STATE_VECTOR_OR_DENSITY_MATRIX


@dataclass
class StateAndMeasurements:
    state: TYPE_STATE_VECTOR_OR_DENSITY_MATRIX
    measurements: dict[int, list[int]] = field(default_factory=lambda: defaultdict(list))

    def __eq__(self, other):
        return allclose(self.state, other.state, atol=1e-7) and self.measurements == other.measurements
