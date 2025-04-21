from numpy import allclose

from stim_experiments.utilities import TYPE_STATE_VECTOR_OR_DENSITY_MATRIX


def states_are_equal(state1: TYPE_STATE_VECTOR_OR_DENSITY_MATRIX, state2: TYPE_STATE_VECTOR_OR_DENSITY_MATRIX) -> bool:
    return allclose(state1, state2, atol=1e-7)
