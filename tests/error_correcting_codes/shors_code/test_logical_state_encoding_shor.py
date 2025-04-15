from numpy import allclose

from stim_experiments.error_correcting_codes.shors_code.shors_repetition_code import ShorsRepetitionCode
from stim_experiments.utilities import KET_ONE_DENSITY_MATRIX, KET_ZERO_DENSITY_MATRIX
from tests.error_correcting_codes.shors_code.expected_states_shor import ExpectedStatesShor


class TestLogicalStateEncodingShor:
    def test_logical_zero(self):
        expected_state = ExpectedStatesShor().get_logical_zero_density_matrix()
        code = ShorsRepetitionCode(initial_logical_qubit_state=KET_ZERO_DENSITY_MATRIX)
        current_state = code.get_current_state()
        assert allclose(current_state, expected_state, atol=1e-7)

    def test_logical_one(self):
        expected_state = ExpectedStatesShor().get_logical_one_density_matrix()
        code = ShorsRepetitionCode(initial_logical_qubit_state=KET_ONE_DENSITY_MATRIX)
        current_state = code.get_current_state()
        assert allclose(current_state, expected_state, atol=1e-7)
