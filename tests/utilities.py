import numpy as np
from numpy import allclose, sqrt

from stim_experiments.error_correcting_codes.support.cat_state_creator.cat_state_creator_cx_from_first_qubit import \
    CatStateCreatorCxFromFirstQubit
from stim_experiments.error_correcting_codes.support.measurer.measurer_with_single_qubit import MeasurerWithSingleQubit
from stim_experiments.globals.error_correcting_code_configuration import ConfigurationErrorCorrectingCodeManager
from stim_experiments.utilities.utilities import KET_ONE_STATE_VECTOR, KET_ZERO_STATE_VECTOR, TYPE_STATE_VECTOR, \
    TYPE_STATE_VECTOR_OR_DENSITY_MATRIX, tensor


def states_are_equal(state1: TYPE_STATE_VECTOR_OR_DENSITY_MATRIX, state2: TYPE_STATE_VECTOR_OR_DENSITY_MATRIX) -> bool:
    element_wise_division = state1 / state2
    no_nans = element_wise_division[~np.isnan(element_wise_division)]
    positions_are_equal = np.array_equal(np.isclose(state1, 0, atol=1e-7), np.isclose(state2, 0, atol=1e-7))
    has_global_phase = len(no_nans) and positions_are_equal and np.all(np.isclose(no_nans, no_nans[0], 1e-7))
    global_phase = no_nans[0] if has_global_phase else 1  # TODO test global phase check
    return allclose(state1 / global_phase, state2, atol=1e-7)


def get_cat_state_vector(num_qubits: int) -> TYPE_STATE_VECTOR:
    return (1 / sqrt(2)) * (tensor(*[KET_ZERO_STATE_VECTOR] * num_qubits) + tensor(*[KET_ONE_STATE_VECTOR] * num_qubits))


def set_configuration_to_reduce_ancilla_qubits():
    configuration = ConfigurationErrorCorrectingCodeManager.get_configuration()
    configuration.cat_state_creator_type = CatStateCreatorCxFromFirstQubit
    configuration.measurer_type = MeasurerWithSingleQubit
