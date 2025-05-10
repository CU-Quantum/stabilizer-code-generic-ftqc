from cirq import density_matrix_from_state_vector
from numpy import sqrt

from stim_experiments.utilities import TYPE_DENSITY_MATRIX, KET_ONE_STATE_VECTOR, KET_ZERO_STATE_VECTOR, \
    get_ket_cat_state_vector, tensor
from tests.error_correcting_codes.five_qubit_code.expected_states_five_qubit import ExpectedStatesFiveQubit


class ExpectedStatesShor(ExpectedStatesFiveQubit):
    def get_logical_zero_density_matrix(self) -> TYPE_DENSITY_MATRIX:
        GHZ_3 = get_ket_cat_state_vector(num_qubits=3)
        data_qubits = tensor(*[GHZ_3] * 3)
        return density_matrix_from_state_vector(data_qubits)

    def get_logical_one_density_matrix(self) -> TYPE_DENSITY_MATRIX:
        GHZ_3_MINUS = (1 / sqrt(2)) * (tensor(KET_ZERO_STATE_VECTOR, KET_ZERO_STATE_VECTOR, KET_ZERO_STATE_VECTOR)
                                 - tensor(KET_ONE_STATE_VECTOR, KET_ONE_STATE_VECTOR, KET_ONE_STATE_VECTOR))
        data_qubits = tensor(GHZ_3_MINUS, GHZ_3_MINUS, GHZ_3_MINUS)
        return density_matrix_from_state_vector(data_qubits)
