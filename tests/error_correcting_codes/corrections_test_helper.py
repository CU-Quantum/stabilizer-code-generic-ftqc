from cirq import Circuit, DensityMatrixSimulator, DensityMatrixTrialResult, Gate, LineQubit
from numpy import allclose, log2

from stim_experiments.error_correcting_codes.error_correcting_code.error_correcting_code import ErrorCorrectingCode
from tests.error_correcting_codes.expected_states_utilities import ExpectedStatesUtilities


class CorrectionsTestHelper:
    def __init__(self, expected_states_utilities: ExpectedStatesUtilities, code: ErrorCorrectingCode):
        self._expected_states_utilities = expected_states_utilities
        self._code = code

    def error_is_corrected(self, error_gate: Gate, qubit_index: int) -> bool:
        self._code.get_error_circuit(error_gate, qubit_index=qubit_index)
        self._code.correct_errors()
        current_state = self._code.get_current_state()

        expected_state = self._expected_states_utilities.get_logical_zero_density_matrix()
        return allclose(current_state, expected_state, atol=1e-7)
