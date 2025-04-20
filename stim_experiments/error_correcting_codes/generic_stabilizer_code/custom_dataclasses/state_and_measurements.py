from dataclasses import dataclass

from numpy._typing import NDArray
from numpy.ma import allclose, allequal

from stim_experiments.utilities import TYPE_STATE_VECTOR_OR_DENSITY_MATRIX


@dataclass
class StateAndMeasurements:
    state: TYPE_STATE_VECTOR_OR_DENSITY_MATRIX
    measurements: NDArray[bool]

    def __eq__(self, other):
        return allclose(self.state, other.state, atol=1e-7) and allequal(self.measurements, other.measurements)
