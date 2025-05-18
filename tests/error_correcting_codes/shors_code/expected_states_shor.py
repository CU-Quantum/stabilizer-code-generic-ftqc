from numpy import sqrt

from stim_experiments.utilities.utilities import KET_ONE_STATE_VECTOR, KET_ZERO_STATE_VECTOR, TYPE_STATE_VECTOR, \
    get_ket_cat_state_vector, \
    tensor
from tests.error_correcting_codes.expected_states.expected_states import ExpectedStates


class ExpectedStatesShor(ExpectedStates):
    def get_logical_zero_state_vector(self) -> TYPE_STATE_VECTOR:
        GHZ_3 = get_ket_cat_state_vector(num_qubits=3)
        return tensor(*[GHZ_3] * 3)

    def get_logical_one_state_vector(self) -> TYPE_STATE_VECTOR:
        GHZ_3_MINUS = (1 / sqrt(2)) * (tensor(KET_ZERO_STATE_VECTOR, KET_ZERO_STATE_VECTOR, KET_ZERO_STATE_VECTOR)
                                       - tensor(KET_ONE_STATE_VECTOR, KET_ONE_STATE_VECTOR, KET_ONE_STATE_VECTOR))
        return tensor(GHZ_3_MINUS, GHZ_3_MINUS, GHZ_3_MINUS)
