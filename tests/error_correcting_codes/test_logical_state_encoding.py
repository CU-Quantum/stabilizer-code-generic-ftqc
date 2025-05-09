import pytest

from stim_experiments.error_correcting_codes.five_qubit_code.five_qubit_code import FiveQubitCode
from stim_experiments.error_correcting_codes.generic_stabilizer_code.generic_stabilizer_code import \
    GenericStabilizerCode
from stim_experiments.error_correcting_codes.shors_code.shors_repetition_code import ShorsRepetitionCode
from stim_experiments.error_correcting_codes.steane_code.staene_code import SteaneCode
from stim_experiments.utilities import KET_ONE_DENSITY_MATRIX, KET_ONE_STATE_VECTOR, KET_ZERO_DENSITY_MATRIX, \
    KET_ZERO_STATE_VECTOR, TYPE_STATE_VECTOR_OR_DENSITY_MATRIX
from tests.error_correcting_codes.five_qubit_code.expected_states_five_qubit import ExpectedStatesFiveQubit
from tests.error_correcting_codes.generic_stabilizer_code.expected_states_generic_5_qubit import \
    ExpectedStatesGenericFiveQubit
from tests.error_correcting_codes.generic_stabilizer_code.utilities import get_check_matrix_values_5_qubit
from tests.error_correcting_codes.shors_code.expected_states_shor import ExpectedStatesShor
from tests.error_correcting_codes.steane_code.expected_states_steane import ExpectedStatesSteane
from tests.error_correcting_codes.three_cat_code.expected_states_three_cat import ExpectedStatesThreeCat
from tests.utilities import states_are_equal


class ThreeCatCode:
    pass


class TestLogicalStateEncoding:
    @pytest.mark.parametrize('code, expected_state', [
        (
                ThreeCatCode(initial_logical_qubit_state=KET_ZERO_STATE_VECTOR),
                ExpectedStatesThreeCat().get_logical_zero_state_vector()
        ),
        (
                FiveQubitCode(initial_logical_qubit_state=KET_ZERO_DENSITY_MATRIX),
                ExpectedStatesFiveQubit().get_logical_zero_density_matrix()
        ),
        # (
        #         GenericStabilizerCode(generators=get_check_matrix_values_steane(), initial_logical_qubit_state=KET_ZERO_DENSITY_MATRIX),
        #         ExpectedStatesGenericSteane().get_logical_zero_density_matrix()
        # ),
        (
                GenericStabilizerCode(generators=get_check_matrix_values_5_qubit(), initial_logical_qubit_state=KET_ZERO_DENSITY_MATRIX),
                ExpectedStatesGenericFiveQubit().get_logical_zero_density_matrix()
        ),
        (
                ShorsRepetitionCode(initial_logical_qubit_state=KET_ZERO_DENSITY_MATRIX),
                ExpectedStatesShor().get_logical_zero_density_matrix()
        ),
        (
                SteaneCode(initial_logical_qubit_state=KET_ZERO_DENSITY_MATRIX),
                ExpectedStatesSteane().get_logical_zero_density_matrix()
        ),
    ])
    def test_logical_zero(self, code: FiveQubitCode, expected_state: TYPE_STATE_VECTOR_OR_DENSITY_MATRIX):
        current_state = code.encode_logical_qubit()
        assert states_are_equal(current_state, expected_state)

    @pytest.mark.parametrize('code, expected_state', [
        (
                ThreeCatCode(initial_logical_qubit_state=KET_ONE_STATE_VECTOR),
                ExpectedStatesThreeCat().get_logical_one_state_vector()
        ),
        (
                FiveQubitCode(initial_logical_qubit_state=KET_ONE_DENSITY_MATRIX),
                ExpectedStatesFiveQubit().get_logical_one_density_matrix(),
        ),
        (
                GenericStabilizerCode(generators=get_check_matrix_values_5_qubit(), initial_logical_qubit_state=KET_ONE_DENSITY_MATRIX),
                ExpectedStatesGenericFiveQubit().get_logical_one_density_matrix()
        ),
        (
                ShorsRepetitionCode(initial_logical_qubit_state=KET_ONE_DENSITY_MATRIX),
                ExpectedStatesShor().get_logical_one_density_matrix()
        ),
        (
                SteaneCode(initial_logical_qubit_state=KET_ONE_DENSITY_MATRIX),
                ExpectedStatesSteane().get_logical_one_density_matrix()
        ),
    ])
    def test_logical_one(self, code: FiveQubitCode, expected_state: TYPE_STATE_VECTOR_OR_DENSITY_MATRIX):
        current_state = code.encode_logical_qubit()
        assert states_are_equal(current_state, expected_state)
