import pytest
from numpy import allclose

from stim_experiments.error_correcting_codes.generic_stabilizer_code.generic_stabilizer_code import GenericStabilizerCode
from stim_experiments.utilities import KET_ONE_DENSITY_MATRIX, KET_ZERO_DENSITY_MATRIX, \
    partial_trace
from tests.error_correcting_codes.five_qubit_code.expected_states_five_qubit import ExpectedStatesFiveQubit
from tests.error_correcting_codes.generic_stabilizer_code.utilities import get_check_matrix_values_4_qubit, \
    get_check_matrix_values_5_qubit, \
    get_check_matrix_values_steane
from tests.error_correcting_codes.steane_code.expected_states_steane import ExpectedStatesSteane


class TestGenericStabilizerCode:
    def test_logical_zero_steane(self):
        size_of_code_plus_one_ancilla = 8
        expected_state = partial_trace(ExpectedStatesSteane().get_logical_zero_density_matrix(), list(range(size_of_code_plus_one_ancilla)))
        code = GenericStabilizerCode(generators=get_check_matrix_values_steane())
        current_state = code.get_current_state()
        assert allclose(current_state, expected_state, atol=1e-7)

    def test_logical_zero_five_qubit(self):
        size_of_code_plus_one_ancilla = 6
        expected_state = partial_trace(ExpectedStatesFiveQubit().get_logical_zero_density_matrix(), list(range(size_of_code_plus_one_ancilla)))
        code = GenericStabilizerCode(generators=get_check_matrix_values_5_qubit())
        current_state = code.get_current_state()
        assert allclose(current_state, expected_state, atol=1e-7)

    def test_logical_one_five_qubit(self):
        size_of_code_plus_one_ancilla = 6
        expected_state = partial_trace(ExpectedStatesFiveQubit().get_logical_one_density_matrix(), list(range(size_of_code_plus_one_ancilla)))
        code = GenericStabilizerCode(generators=get_check_matrix_values_5_qubit(), initial_logical_qubit_state_density_matrix=KET_ONE_DENSITY_MATRIX)
        current_state = code.get_current_state()
        assert allclose(current_state, expected_state, atol=1e-7)

    def test_input_state_must_be_size_of_logical_qubits_for_code(self):
        code_that_encodes_two_logical_bits = get_check_matrix_values_4_qubit()
        logical_qubit_state_of_only_one_qubit = KET_ZERO_DENSITY_MATRIX
        with pytest.raises(ValueError, match="These generators encode 2 logical qubits, but an initial state of 1 was given."):
            GenericStabilizerCode(generators=code_that_encodes_two_logical_bits,
                                  initial_logical_qubit_state_density_matrix=logical_qubit_state_of_only_one_qubit)
