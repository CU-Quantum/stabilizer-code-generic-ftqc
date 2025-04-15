import pytest
from numpy import allclose

from stim_experiments.error_correcting_codes.generic_stabilizer_code.generic_stabilizer_code import GenericStabilizerCode
from stim_experiments.utilities import KET_ONE_DENSITY_MATRIX, KET_ZERO_DENSITY_MATRIX
from tests.error_correcting_codes.generic_stabilizer_code.expected_states_generic_5_qubit import \
    ExpectedStatesGenericFiveQubit
from tests.error_correcting_codes.generic_stabilizer_code.expected_states_generic_steane import \
    ExpectedStatesGenericSteane
from tests.error_correcting_codes.generic_stabilizer_code.utilities import get_check_matrix_values_4_qubit, \
    get_check_matrix_values_5_qubit, \
    get_check_matrix_values_steane


class TestGenericStabilizerCodeGeneralStabilizer:
    def test_logical_zero_steane(self):
        code = GenericStabilizerCode(generators=get_check_matrix_values_steane(), initial_logical_qubit_state=KET_ZERO_DENSITY_MATRIX)
        current_state = code.get_current_state()
        expected_state = ExpectedStatesGenericSteane().get_logical_zero_density_matrix()
        assert allclose(current_state, expected_state, atol=1e-7)

    def test_logical_zero_five_qubit(self):
        code = GenericStabilizerCode(generators=get_check_matrix_values_5_qubit(), initial_logical_qubit_state=KET_ZERO_DENSITY_MATRIX)
        current_state = code.get_current_state()
        expected_state = ExpectedStatesGenericFiveQubit().get_logical_zero_density_matrix()
        assert allclose(current_state, expected_state, atol=1e-7)

    def test_logical_one_five_qubit(self):
        code = GenericStabilizerCode(generators=get_check_matrix_values_5_qubit(), initial_logical_qubit_state=KET_ONE_DENSITY_MATRIX)
        current_state = code.get_current_state()
        expected_state = ExpectedStatesGenericFiveQubit().get_logical_one_density_matrix()
        assert allclose(current_state, expected_state, atol=1e-7)

    def test_input_state_must_be_size_of_logical_qubits_for_code(self):
        code_that_encodes_two_logical_bits = get_check_matrix_values_4_qubit()
        logical_qubit_state_of_only_one_qubit = KET_ZERO_DENSITY_MATRIX
        with pytest.raises(ValueError, match="These generators encode 2 logical qubits, but an initial state of 1 was given."):
            GenericStabilizerCode(generators=code_that_encodes_two_logical_bits,
                                  initial_logical_qubit_state=logical_qubit_state_of_only_one_qubit)
