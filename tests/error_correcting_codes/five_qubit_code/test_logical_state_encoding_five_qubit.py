from stim_experiments.error_correcting_codes.five_qubit_code.five_qubit_code import FiveQubitCode
from stim_experiments.utilities import KET_ONE_DENSITY_MATRIX, KET_ZERO_DENSITY_MATRIX
from tests.error_correcting_codes.five_qubit_code.expected_states_five_qubit import ExpectedStatesFiveQubit
from tests.utilities import states_are_equal


class TestLogicalStateEncodingSteane:
    def test_logical_zero(self):
        expected_state = ExpectedStatesFiveQubit().get_logical_zero_density_matrix()
        code = FiveQubitCode(initial_logical_qubit_state=KET_ZERO_DENSITY_MATRIX)
        current_state = code.encode_logical_qubit()
        assert states_are_equal(current_state, expected_state)

    def test_logical_one(self):
        expected_state = ExpectedStatesFiveQubit().get_logical_one_density_matrix()
        code = FiveQubitCode(initial_logical_qubit_state=KET_ONE_DENSITY_MATRIX)
        current_state = code.encode_logical_qubit()
        assert states_are_equal(current_state, expected_state)
