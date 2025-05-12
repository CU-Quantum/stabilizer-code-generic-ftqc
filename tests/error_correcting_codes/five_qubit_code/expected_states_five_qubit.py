from cirq import density_matrix_from_state_vector

from stim_experiments.utilities import TYPE_DENSITY_MATRIX, KET_ONE_STATE_VECTOR, KET_ZERO_STATE_VECTOR, tensor


class ExpectedStatesFiveQubit:
    def get_logical_zero_density_matrix(self) -> TYPE_DENSITY_MATRIX:
        return density_matrix_from_state_vector(state_vector=self.get_logical_zero_state_vector())

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

    def get_logical_one_density_matrix(self) -> TYPE_DENSITY_MATRIX:
        return density_matrix_from_state_vector(state_vector=self.get_logical_one_state_vector())

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
