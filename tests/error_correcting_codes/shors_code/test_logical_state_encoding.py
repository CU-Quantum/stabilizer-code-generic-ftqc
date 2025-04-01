from numpy.ma.core import allclose

from stim_experiments.error_correcting_codes.shors_code.shors_repetition_code import ShorsRepetitionCode
from stim_experiments.utilities import DENSITY_MATRIX_TYPE, KET_ONE_DENSITY_MATRIX, KET_ZERO_DENSITY_MATRIX
from tests.error_correcting_codes.shors_code.expected_states import ExpectedStatesUtilities


class TestLogicalStateEncoding:
    _expected_states_utilities = ExpectedStatesUtilities()

    def test_logical_zero(self):
        assert self._encoding_matches_expected(initial_state=KET_ZERO_DENSITY_MATRIX, expected_state=self._expected_state_zero)

    def test_logical_one(self):
        assert self._encoding_matches_expected(initial_state=KET_ONE_DENSITY_MATRIX, expected_state=self._expected_state_one)

    @staticmethod
    def _encoding_matches_expected(initial_state: DENSITY_MATRIX_TYPE, expected_state: DENSITY_MATRIX_TYPE) -> DENSITY_MATRIX_TYPE:
        code = ShorsRepetitionCode(initial_qubit_state_density_matrix=initial_state)
        current_state = code.get_current_state()
        return allclose(current_state, expected_state, atol=1e-14)

    @property
    def _expected_state_zero(self) -> DENSITY_MATRIX_TYPE:
        circuit = self._expected_states_utilities.get_logical_zero_circuit()
        return self._expected_states_utilities.get_expected_state(circuit)

    @property
    def _expected_state_one(self) -> DENSITY_MATRIX_TYPE:
        circuit = self._expected_states_utilities.get_logical_one_circuit()
        return self._expected_states_utilities.get_expected_state(circuit)
