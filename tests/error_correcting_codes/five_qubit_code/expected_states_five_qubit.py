from cirq import density_matrix_from_state_vector

from stim_experiments.utilities import TYPE_DENSITY_MATRIX, KET_ONE_STATE_VECTOR, KET_ZERO_STATE_VECTOR, tensor
from tests.error_correcting_codes.expected_states.expected_states import ExpectedStates


class ExpectedStatesFiveQubit(ExpectedStates):
    def get_logical_zero_state_vector(self) -> TYPE_DENSITY_MATRIX:
        return (1/4) * (
                tensor(*[KET_ZERO_STATE_VECTOR] * 5)
                + tensor(KET_ONE_STATE_VECTOR,
                        KET_ZERO_STATE_VECTOR,
                        KET_ZERO_STATE_VECTOR,
                        KET_ONE_STATE_VECTOR,
                        KET_ZERO_STATE_VECTOR)
                + tensor(KET_ZERO_STATE_VECTOR,
                        KET_ONE_STATE_VECTOR,
                        KET_ZERO_STATE_VECTOR,
                        KET_ZERO_STATE_VECTOR,
                        KET_ONE_STATE_VECTOR)
                + tensor(KET_ONE_STATE_VECTOR,
                        KET_ZERO_STATE_VECTOR,
                        KET_ONE_STATE_VECTOR,
                        KET_ZERO_STATE_VECTOR,
                        KET_ZERO_STATE_VECTOR)
                + tensor(KET_ZERO_STATE_VECTOR,
                        KET_ONE_STATE_VECTOR,
                        KET_ZERO_STATE_VECTOR,
                        KET_ONE_STATE_VECTOR,
                        KET_ZERO_STATE_VECTOR)
                - tensor(KET_ONE_STATE_VECTOR,
                        KET_ONE_STATE_VECTOR,
                        KET_ZERO_STATE_VECTOR,
                        KET_ONE_STATE_VECTOR,
                        KET_ONE_STATE_VECTOR)
                - tensor(KET_ZERO_STATE_VECTOR,
                        KET_ZERO_STATE_VECTOR,
                        KET_ONE_STATE_VECTOR,
                        KET_ONE_STATE_VECTOR,
                        KET_ZERO_STATE_VECTOR)
                - tensor(KET_ONE_STATE_VECTOR,
                        KET_ONE_STATE_VECTOR,
                        KET_ZERO_STATE_VECTOR,
                        KET_ZERO_STATE_VECTOR,
                        KET_ZERO_STATE_VECTOR)
                - tensor(KET_ONE_STATE_VECTOR,
                        KET_ONE_STATE_VECTOR,
                        KET_ONE_STATE_VECTOR,
                        KET_ZERO_STATE_VECTOR,
                        KET_ONE_STATE_VECTOR)
                - tensor(KET_ZERO_STATE_VECTOR,
                        KET_ZERO_STATE_VECTOR,
                        KET_ZERO_STATE_VECTOR,
                        KET_ONE_STATE_VECTOR,
                        KET_ONE_STATE_VECTOR)
                - tensor(KET_ONE_STATE_VECTOR,
                        KET_ONE_STATE_VECTOR,
                        KET_ONE_STATE_VECTOR,
                        KET_ONE_STATE_VECTOR,
                        KET_ZERO_STATE_VECTOR)
                - tensor(KET_ZERO_STATE_VECTOR,
                        KET_ONE_STATE_VECTOR,
                        KET_ONE_STATE_VECTOR,
                        KET_ONE_STATE_VECTOR,
                        KET_ONE_STATE_VECTOR)
                - tensor(KET_ONE_STATE_VECTOR,
                        KET_ZERO_STATE_VECTOR,
                        KET_ZERO_STATE_VECTOR,
                        KET_ZERO_STATE_VECTOR,
                        KET_ONE_STATE_VECTOR)
                - tensor(KET_ZERO_STATE_VECTOR,
                        KET_ONE_STATE_VECTOR,
                        KET_ONE_STATE_VECTOR,
                        KET_ZERO_STATE_VECTOR,
                        KET_ZERO_STATE_VECTOR)
                - tensor(KET_ONE_STATE_VECTOR,
                        KET_ZERO_STATE_VECTOR,
                        KET_ONE_STATE_VECTOR,
                        KET_ONE_STATE_VECTOR,
                        KET_ONE_STATE_VECTOR)
                + tensor(KET_ZERO_STATE_VECTOR,
                        KET_ZERO_STATE_VECTOR,
                        KET_ONE_STATE_VECTOR,
                        KET_ZERO_STATE_VECTOR,
                        KET_ONE_STATE_VECTOR)
        )

    def get_logical_one_state_vector(self) -> TYPE_DENSITY_MATRIX:
        return (1 / 4) * (
                tensor(*[KET_ONE_STATE_VECTOR] * 5)
                + tensor(KET_ZERO_STATE_VECTOR,
                       KET_ONE_STATE_VECTOR,
                       KET_ONE_STATE_VECTOR,
                       KET_ZERO_STATE_VECTOR,
                       KET_ONE_STATE_VECTOR)
                + tensor(KET_ONE_STATE_VECTOR,
                       KET_ZERO_STATE_VECTOR,
                       KET_ONE_STATE_VECTOR,
                       KET_ONE_STATE_VECTOR,
                       KET_ZERO_STATE_VECTOR)
                + tensor(KET_ZERO_STATE_VECTOR,
                       KET_ONE_STATE_VECTOR,
                       KET_ZERO_STATE_VECTOR,
                       KET_ONE_STATE_VECTOR,
                       KET_ONE_STATE_VECTOR)
                + tensor(KET_ONE_STATE_VECTOR,
                       KET_ZERO_STATE_VECTOR,
                       KET_ONE_STATE_VECTOR,
                       KET_ZERO_STATE_VECTOR,
                       KET_ONE_STATE_VECTOR)
                - tensor(KET_ZERO_STATE_VECTOR,
                       KET_ZERO_STATE_VECTOR,
                       KET_ONE_STATE_VECTOR,
                       KET_ZERO_STATE_VECTOR,
                       KET_ZERO_STATE_VECTOR)
                - tensor(KET_ONE_STATE_VECTOR,
                       KET_ONE_STATE_VECTOR,
                       KET_ZERO_STATE_VECTOR,
                       KET_ZERO_STATE_VECTOR,
                       KET_ONE_STATE_VECTOR)
                - tensor(KET_ZERO_STATE_VECTOR,
                       KET_ZERO_STATE_VECTOR,
                       KET_ONE_STATE_VECTOR,
                       KET_ONE_STATE_VECTOR,
                       KET_ONE_STATE_VECTOR)
                - tensor(KET_ZERO_STATE_VECTOR,
                       KET_ZERO_STATE_VECTOR,
                       KET_ZERO_STATE_VECTOR,
                       KET_ONE_STATE_VECTOR,
                       KET_ZERO_STATE_VECTOR)
                - tensor(KET_ONE_STATE_VECTOR,
                       KET_ONE_STATE_VECTOR,
                       KET_ONE_STATE_VECTOR,
                       KET_ZERO_STATE_VECTOR,
                       KET_ZERO_STATE_VECTOR)
                - tensor(KET_ZERO_STATE_VECTOR,
                       KET_ZERO_STATE_VECTOR,
                       KET_ZERO_STATE_VECTOR,
                       KET_ZERO_STATE_VECTOR,
                       KET_ONE_STATE_VECTOR)
                - tensor(KET_ONE_STATE_VECTOR,
                       KET_ZERO_STATE_VECTOR,
                       KET_ZERO_STATE_VECTOR,
                       KET_ZERO_STATE_VECTOR,
                       KET_ZERO_STATE_VECTOR)
                - tensor(KET_ZERO_STATE_VECTOR,
                       KET_ONE_STATE_VECTOR,
                       KET_ONE_STATE_VECTOR,
                       KET_ONE_STATE_VECTOR,
                       KET_ZERO_STATE_VECTOR)
                - tensor(KET_ONE_STATE_VECTOR,
                       KET_ZERO_STATE_VECTOR,
                       KET_ZERO_STATE_VECTOR,
                       KET_ONE_STATE_VECTOR,
                       KET_ONE_STATE_VECTOR)
                - tensor(KET_ZERO_STATE_VECTOR,
                       KET_ONE_STATE_VECTOR,
                       KET_ZERO_STATE_VECTOR,
                       KET_ZERO_STATE_VECTOR,
                       KET_ZERO_STATE_VECTOR)
                + tensor(KET_ONE_STATE_VECTOR,
                       KET_ONE_STATE_VECTOR,
                       KET_ZERO_STATE_VECTOR,
                       KET_ONE_STATE_VECTOR,
                       KET_ZERO_STATE_VECTOR)
        )
