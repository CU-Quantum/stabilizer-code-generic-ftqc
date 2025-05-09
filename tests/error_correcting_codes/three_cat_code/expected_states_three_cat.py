from cirq import Circuit, I, LineQubit, Simulator, Z, density_matrix_from_state_vector

from stim_experiments.utilities import TYPE_DENSITY_MATRIX, tensor
from tests.error_correcting_codes.expected_states_utilities import ExpectedStatesUtilities
from tests.utilities import get_cat_state_vector


class ExpectedStatesThreeCat(ExpectedStatesUtilities):
    _num_repetitions = 3

    def get_logical_zero_density_matrix(self) -> TYPE_DENSITY_MATRIX:
        return density_matrix_from_state_vector(self.get_logical_zero_state_vector())

    def get_logical_zero_state_vector(self) -> TYPE_DENSITY_MATRIX:
        arbitrary_num_qubits = 4
        return tensor(*[get_cat_state_vector(num_qubits=arbitrary_num_qubits)] * self._num_repetitions)

    def get_logical_one_density_matrix(self) -> TYPE_DENSITY_MATRIX:
        return density_matrix_from_state_vector(self.get_logical_one_state_vector())

    def get_logical_one_state_vector(self) -> TYPE_DENSITY_MATRIX:
        arbitrary_num_qubits = 4
        one_cat_state = get_cat_state_vector(num_qubits=arbitrary_num_qubits)
        one_cat_state_flipped_sign = Simulator().simulate(Circuit(
            [I(LineQubit(i)) for i in range(arbitrary_num_qubits)],
            Z(LineQubit(0)),
        )).final_state_vector
        return tensor(*[one_cat_state_flipped_sign] * self._num_repetitions)
