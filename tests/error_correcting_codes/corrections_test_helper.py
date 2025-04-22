from cirq import Circuit, Gate

from stim_experiments.error_correcting_codes.error_correcting_code.error_correcting_code import ErrorCorrectingCode
from tests.error_correcting_codes.expected_states_utilities import ExpectedStatesUtilities
from tests.utilities import states_are_equal


class CorrectionsTestHelper:
    def __init__(self, expected_states_utilities: ExpectedStatesUtilities, code: ErrorCorrectingCode):
        self._expected_states_utilities = expected_states_utilities
        self._code = code

    def error_is_corrected(self, error_gate: Gate, qubit_index: int) -> bool:
        state = self._code.encode_logical_qubit()
        circuit = Circuit(
            self._code.get_error_circuit(error_gate, qubit_index=qubit_index),
            self._code.get_error_correction_circuit()
        )
        current_state = self._code.error_correcting_code_utilities.get_state_after_circuit(circuit=circuit,
                                                                                   qubit_order=self._code.all_qubits,
                                                                                   initial_state=state)
        expected_state = self._expected_states_utilities.get_logical_zero_density_matrix()
        return states_are_equal(current_state.state, expected_state)
