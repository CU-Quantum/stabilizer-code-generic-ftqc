from cirq import density_matrix_from_state_vector, kron
from numpy import sqrt

from stim_experiments.utilities import DENSITY_MATRIX_TYPE, KET_ONE_STATE_VECTOR, KET_ZERO_STATE_VECTOR
from tests.error_correcting_codes.five_qubit_code.expected_states_five_qubit import ExpectedStatesFiveQubit


class ExpectedStatesSteane(ExpectedStatesFiveQubit):
    _num_ancillas = 3

    def get_logical_zero_density_matrix(self) -> DENSITY_MATRIX_TYPE:
        data_qubits = (1/sqrt(8)) * (
                kron(*[KET_ZERO_STATE_VECTOR] * 7)
                + kron(KET_ONE_STATE_VECTOR,
                        KET_ZERO_STATE_VECTOR,
                        KET_ONE_STATE_VECTOR,
                        KET_ZERO_STATE_VECTOR,
                        KET_ONE_STATE_VECTOR,
                        KET_ZERO_STATE_VECTOR,
                        KET_ONE_STATE_VECTOR)
                + kron(KET_ZERO_STATE_VECTOR,
                        KET_ONE_STATE_VECTOR,
                        KET_ONE_STATE_VECTOR,
                        KET_ZERO_STATE_VECTOR,
                        KET_ZERO_STATE_VECTOR,
                        KET_ONE_STATE_VECTOR,
                        KET_ONE_STATE_VECTOR)
                + kron(KET_ONE_STATE_VECTOR,
                        KET_ONE_STATE_VECTOR,
                        KET_ZERO_STATE_VECTOR,
                        KET_ZERO_STATE_VECTOR,
                        KET_ONE_STATE_VECTOR,
                        KET_ONE_STATE_VECTOR,
                        KET_ZERO_STATE_VECTOR)
                + kron(KET_ZERO_STATE_VECTOR,
                        KET_ZERO_STATE_VECTOR,
                        KET_ZERO_STATE_VECTOR,
                        KET_ONE_STATE_VECTOR,
                        KET_ONE_STATE_VECTOR,
                        KET_ONE_STATE_VECTOR,
                        KET_ONE_STATE_VECTOR)
                + kron(KET_ONE_STATE_VECTOR,
                        KET_ZERO_STATE_VECTOR,
                        KET_ONE_STATE_VECTOR,
                        KET_ONE_STATE_VECTOR,
                        KET_ZERO_STATE_VECTOR,
                        KET_ONE_STATE_VECTOR,
                        KET_ZERO_STATE_VECTOR)
                + kron(KET_ZERO_STATE_VECTOR,
                        KET_ONE_STATE_VECTOR,
                        KET_ONE_STATE_VECTOR,
                        KET_ONE_STATE_VECTOR,
                        KET_ONE_STATE_VECTOR,
                        KET_ZERO_STATE_VECTOR,
                        KET_ZERO_STATE_VECTOR)
                + kron(KET_ONE_STATE_VECTOR,
                        KET_ONE_STATE_VECTOR,
                        KET_ZERO_STATE_VECTOR,
                        KET_ONE_STATE_VECTOR,
                        KET_ZERO_STATE_VECTOR,
                        KET_ZERO_STATE_VECTOR,
                        KET_ONE_STATE_VECTOR)
        )
        ancilla_qubits = kron(*[KET_ZERO_STATE_VECTOR] * self._num_ancillas)
        state_vector = kron(data_qubits, ancilla_qubits)
        return density_matrix_from_state_vector(state_vector=state_vector)

    def get_logical_one_density_matrix(self) -> DENSITY_MATRIX_TYPE:
        data_qubits = (1 / sqrt(8)) * (
                kron(*[KET_ONE_STATE_VECTOR] * 7)
                + kron(KET_ZERO_STATE_VECTOR,
                       KET_ONE_STATE_VECTOR,
                       KET_ZERO_STATE_VECTOR,
                       KET_ONE_STATE_VECTOR,
                       KET_ZERO_STATE_VECTOR,
                       KET_ONE_STATE_VECTOR,
                       KET_ZERO_STATE_VECTOR)
                + kron(KET_ONE_STATE_VECTOR,
                       KET_ZERO_STATE_VECTOR,
                       KET_ZERO_STATE_VECTOR,
                       KET_ONE_STATE_VECTOR,
                       KET_ONE_STATE_VECTOR,
                       KET_ZERO_STATE_VECTOR,
                       KET_ZERO_STATE_VECTOR)
                + kron(KET_ZERO_STATE_VECTOR,
                       KET_ZERO_STATE_VECTOR,
                       KET_ONE_STATE_VECTOR,
                       KET_ONE_STATE_VECTOR,
                       KET_ZERO_STATE_VECTOR,
                       KET_ZERO_STATE_VECTOR,
                       KET_ONE_STATE_VECTOR)
                + kron(KET_ONE_STATE_VECTOR,
                       KET_ONE_STATE_VECTOR,
                       KET_ONE_STATE_VECTOR,
                       KET_ZERO_STATE_VECTOR,
                       KET_ZERO_STATE_VECTOR,
                       KET_ZERO_STATE_VECTOR,
                       KET_ZERO_STATE_VECTOR)
                + kron(KET_ZERO_STATE_VECTOR,
                       KET_ONE_STATE_VECTOR,
                       KET_ZERO_STATE_VECTOR,
                       KET_ZERO_STATE_VECTOR,
                       KET_ONE_STATE_VECTOR,
                       KET_ZERO_STATE_VECTOR,
                       KET_ONE_STATE_VECTOR)
                + kron(KET_ONE_STATE_VECTOR,
                       KET_ZERO_STATE_VECTOR,
                       KET_ZERO_STATE_VECTOR,
                       KET_ZERO_STATE_VECTOR,
                       KET_ZERO_STATE_VECTOR,
                       KET_ONE_STATE_VECTOR,
                       KET_ONE_STATE_VECTOR)
                + kron(KET_ZERO_STATE_VECTOR,
                       KET_ZERO_STATE_VECTOR,
                       KET_ONE_STATE_VECTOR,
                       KET_ZERO_STATE_VECTOR,
                       KET_ONE_STATE_VECTOR,
                       KET_ONE_STATE_VECTOR,
                       KET_ZERO_STATE_VECTOR)
        )
        ancilla_qubits = kron(*[KET_ZERO_STATE_VECTOR] * self._num_ancillas)
        state_vector = kron(data_qubits, ancilla_qubits)
        return density_matrix_from_state_vector(state_vector=state_vector)
