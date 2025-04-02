from cirq import density_matrix_from_state_vector, kron
from numpy import sqrt

from stim_experiments.utilities import DENSITY_MATRIX_TYPE, KET_ONE_STATE_VECTOR, KET_ZERO_STATE_VECTOR


class ExpectedStatesShor:
    def get_logical_zero_density_matrix(self) -> DENSITY_MATRIX_TYPE:
        GHZ_3 = (1 / sqrt(2)) * (kron(KET_ZERO_STATE_VECTOR, KET_ZERO_STATE_VECTOR, KET_ZERO_STATE_VECTOR)
                                + kron(KET_ONE_STATE_VECTOR, KET_ONE_STATE_VECTOR, KET_ONE_STATE_VECTOR))
        data_qubits = kron(GHZ_3, GHZ_3, GHZ_3)
        ancilla_qubits = kron(KET_ZERO_STATE_VECTOR, KET_ZERO_STATE_VECTOR)
        state_vector = kron(data_qubits, ancilla_qubits)
        return density_matrix_from_state_vector(state_vector)

    def get_logical_one_density_matrix(self) -> DENSITY_MATRIX_TYPE:
        GHZ_3_MINUS = (1 / sqrt(2)) * (kron(KET_ZERO_STATE_VECTOR, KET_ZERO_STATE_VECTOR, KET_ZERO_STATE_VECTOR)
                                 - kron(KET_ONE_STATE_VECTOR, KET_ONE_STATE_VECTOR, KET_ONE_STATE_VECTOR))
        data_qubits = kron(GHZ_3_MINUS, GHZ_3_MINUS, GHZ_3_MINUS)
        ancilla_qubits = kron(KET_ZERO_STATE_VECTOR, KET_ZERO_STATE_VECTOR)
        state_vector = kron(data_qubits, ancilla_qubits)
        return density_matrix_from_state_vector(state_vector)
