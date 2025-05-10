from cirq import Circuit, I, LineQubit, Simulator, Z, density_matrix_from_state_vector

from stim_experiments.utilities import TYPE_DENSITY_MATRIX, tensor
from stim_experiments.error_correcting_codes.three_cat_code.three_cat_code import ThreeCatCode
from tests.utilities import get_cat_state_vector


class ExpectedStatesThreeCat:
    arbitrary_num_qubits = 4
    _num_repetitions = ThreeCatCode.num_cats

    def get_logical_zero_density_matrix(self) -> TYPE_DENSITY_MATRIX:
        return density_matrix_from_state_vector(self.get_logical_zero_state_vector())

    def get_logical_zero_state_vector(self) -> TYPE_DENSITY_MATRIX:
        return tensor(*[get_cat_state_vector(num_qubits=self.arbitrary_num_qubits)] * self._num_repetitions)

    def get_logical_one_density_matrix(self) -> TYPE_DENSITY_MATRIX:
        return density_matrix_from_state_vector(self.get_logical_one_state_vector())

    def get_logical_one_state_vector(self) -> TYPE_DENSITY_MATRIX:
        one_cat_state = get_cat_state_vector(num_qubits=self.arbitrary_num_qubits)
        one_cat_state_flipped_sign = Simulator().simulate(Circuit(
            [I(LineQubit(i)) for i in range(self.arbitrary_num_qubits)],
            Z(LineQubit(0)),
        ), initial_state=one_cat_state).final_state_vector
        return tensor(*[one_cat_state_flipped_sign] * self._num_repetitions)
