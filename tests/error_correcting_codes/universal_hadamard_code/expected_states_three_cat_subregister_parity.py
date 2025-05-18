import numpy as np

from stim_experiments.error_correcting_codes.three_cat_code.three_cat_code import ThreeCatCode
from stim_experiments.utilities.utilities import KET_ONE_STATE_VECTOR, KET_ZERO_STATE_VECTOR, TYPE_STATE_VECTOR, \
    int_to_binary_array, tensor
from tests.error_correcting_codes.expected_states.expected_states import ExpectedStates


class ExpectedStatesThreeCatSubregisterParity(ExpectedStates):
    arbitrary_num_qubits = 4

    def get_logical_zero_state_vector(self) -> TYPE_STATE_VECTOR:
        cat_values_with_even_weight = [cat_values for cat_values in self._all_cat_values if not sum(cat_values) % 2]
        return self._get_logical_state_vector(cat_values=cat_values_with_even_weight)

    def get_logical_one_state_vector(self) -> TYPE_STATE_VECTOR:
        cat_values_with_odd_weight = [cat_values for cat_values in self._all_cat_values if sum(cat_values) % 2]
        return self._get_logical_state_vector(cat_values=cat_values_with_odd_weight)

    def _get_logical_state_vector(self, cat_values: list[list[int]]) -> TYPE_STATE_VECTOR:
        basis_states_by_value = [
            [tensor(*[KET_ONE_STATE_VECTOR if cat_value else KET_ZERO_STATE_VECTOR] * self.arbitrary_num_qubits)
             for cat_value in cat_values]
            for cat_values in cat_values
        ]
        basis_states = [tensor(*states) for states in basis_states_by_value]
        return (1 / 2) * np.sum(basis_states, axis=0)

    @property
    def _all_cat_values(self) -> list[list[int]]:
        return [int_to_binary_array(i, num_elements=ThreeCatCode.num_cats) for i in range(2 ** ThreeCatCode.num_cats)]
