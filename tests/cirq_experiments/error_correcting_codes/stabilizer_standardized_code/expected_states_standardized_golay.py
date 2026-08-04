import pickle
from pathlib import Path

from cirq_experiments.utilities.utilities import TYPE_STATE_VECTOR
from tests.cirq_experiments.error_correcting_codes.expected_states.expected_states import ExpectedStates


class ExpectedStatesGenericGolay(ExpectedStates):
    def get_logical_zero_state_vector(self) -> TYPE_STATE_VECTOR:
        if not hasattr(self, '_logical_zero'):
            path = Path(__file__).parent / 'golay_logical_zero.pkl'
            with open(path, 'rb') as f:
                self._logical_zero = pickle.load(f)
        return self._logical_zero

    def get_logical_one_state_vector(self) -> TYPE_STATE_VECTOR:
        if not hasattr(self, '_logical_one'):
            path = Path(__file__).parent / 'golay_logical_one.pkl'
            with open(path, 'rb') as f:
                self._logical_one = pickle.load(f)
        return self._logical_one
