import pytest
from cirq import X, Y, Z

from stim_experiments.error_correcting_codes.steane_code.staene_code import SteaneCode
from stim_experiments.utilities import KET_ZERO_DENSITY_MATRIX
from tests.error_correcting_codes.corrections_test_helper import CorrectionsTestHelper
from tests.error_correcting_codes.steane_code.expected_states_steane import ExpectedStatesSteane


class TestCorrectionsSteane:
    _expected_states_utilities = ExpectedStatesSteane()
    _arbitrary_qubits = [0, 2, 6]

    @pytest.fixture(autouse=True)
    def _setup(self):
        code = SteaneCode(initial_logical_qubit_state=KET_ZERO_DENSITY_MATRIX)
        self._helper = CorrectionsTestHelper(expected_states_utilities=ExpectedStatesSteane(), code=code)

    @pytest.mark.parametrize('qubit_index', _arbitrary_qubits)
    def test_bit_flip_error_is_corrected(self, qubit_index: int):
        self._helper.error_is_corrected(error_gate=X, qubit_index=qubit_index)

    @pytest.mark.parametrize('qubit_index', _arbitrary_qubits)
    def test_pauli_y_error_is_corrected(self, qubit_index: int):
        self._helper.error_is_corrected(error_gate=Y, qubit_index=qubit_index)
