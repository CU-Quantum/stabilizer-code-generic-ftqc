from cirq import X
from numpy import allclose

from stim_experiments.error_correcting_codes.shors_code.shors_repetition_code import ShorsRepetitionCode
from stim_experiments.utilities import KET_ZERO_DENSITY_MATRIX
from tests.error_correcting_codes.shors_code.expected_states import ExpectedStatesUtilities


class TestCorrections:
    _expected_states_utilities = ExpectedStatesUtilities()

    def test_bit_flip_error_on_qubit_1(self):
        code = ShorsRepetitionCode(initial_qubit_state_density_matrix=KET_ZERO_DENSITY_MATRIX)
        code.apply_bit_flip(qubit_index=0)
        current_state = code.get_current_state()

        circuit = self._expected_states_utilities.get_logical_one_circuit()
        circuit.append(X(self._expected_states_utilities.circuit_qubits[0]))
        expected_state = self._expected_states_utilities.get_expected_state(circuit=circuit)

        assert allclose(current_state, expected_state, atol=1e-7)
