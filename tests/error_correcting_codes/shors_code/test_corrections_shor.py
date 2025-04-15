import pytest
from cirq import X, Y, Z

from stim_experiments.error_correcting_codes.shors_code.shors_repetition_code import ShorsRepetitionCode
from stim_experiments.utilities import KET_ZERO_DENSITY_MATRIX
from tests.error_correcting_codes.corrections_test_helper import CorrectionsTestHelper
from tests.error_correcting_codes.shors_code.expected_states_shor import ExpectedStatesShor


class TestCorrectionsShor:
    _qubit_indices_in_different_positions_in_different_blocks = [0, 4, 8]

    @pytest.fixture(autouse=True)
    def _setup(self):
        code = ShorsRepetitionCode(initial_logical_qubit_state=KET_ZERO_DENSITY_MATRIX)
        self._helper = CorrectionsTestHelper(expected_states_utilities=ExpectedStatesShor(), code=code)

    @pytest.mark.parametrize('qubit_index', _qubit_indices_in_different_positions_in_different_blocks)
    def test_bit_flip_error_is_corrected(self, qubit_index: int):
        self._helper.error_is_corrected(error_gate=X, qubit_index=qubit_index)

    @pytest.mark.parametrize('qubit_index', _qubit_indices_in_different_positions_in_different_blocks)
    def test_phase_flip_error_is_corrected(self, qubit_index: int):
        self._helper.error_is_corrected(error_gate=Z, qubit_index=qubit_index)

    @pytest.mark.parametrize('qubit_index', _qubit_indices_in_different_positions_in_different_blocks)
    def test_pauli_y_error_is_corrected(self, qubit_index: int):
        self._helper.error_is_corrected(error_gate=Y, qubit_index=qubit_index)
