from numpy import sqrt

from stim_experiments.error_correcting_codes.support.cat_state_creator.cat_state_creator_cx_from_first_qubit import \
    CatStateCreatorCxFromFirstQubit
from stim_experiments.error_correcting_codes.support.measurer.measurer_with_single_qubit import MeasurerWithSingleQubit
from stim_experiments.globals.error_correcting_code_configuration import ConfigurationErrorCorrectingCodeManager
from stim_experiments.utilities.utilities import KET_ONE_STATE_VECTOR, KET_ZERO_STATE_VECTOR, TYPE_STATE_VECTOR, \
    tensor


def get_cat_state_vector(num_qubits: int) -> TYPE_STATE_VECTOR:
    return (1 / sqrt(2)) * (tensor(*[KET_ZERO_STATE_VECTOR] * num_qubits) + tensor(*[KET_ONE_STATE_VECTOR] * num_qubits))


def set_configuration_to_reduce_ancilla_qubits():
    configuration = ConfigurationErrorCorrectingCodeManager.get_configuration()
    configuration.cat_state_creator_type = CatStateCreatorCxFromFirstQubit
    configuration.measurer_type = MeasurerWithSingleQubit
