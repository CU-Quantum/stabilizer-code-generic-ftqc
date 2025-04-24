from numpy import allclose, sqrt

from stim_experiments.utilities import KET_ONE_STATE_VECTOR, KET_ZERO_STATE_VECTOR, TYPE_STATE_VECTOR, \
    TYPE_STATE_VECTOR_OR_DENSITY_MATRIX, \
    tensor


def states_are_equal(state1: TYPE_STATE_VECTOR_OR_DENSITY_MATRIX, state2: TYPE_STATE_VECTOR_OR_DENSITY_MATRIX) -> bool:
    return allclose(state1, state2, atol=1e-7)


def get_cat_state_vector(num_qubits: int) -> TYPE_STATE_VECTOR:
    return (1 / sqrt(2)) * (tensor(*[KET_ZERO_STATE_VECTOR] * num_qubits) + tensor(*[KET_ONE_STATE_VECTOR] * num_qubits))
