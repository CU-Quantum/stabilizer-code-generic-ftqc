import pytest

from stim_experiments.error_correcting_codes.generic_stabilizer_code.generic_stabilizer_code import GenericStabilizerCode
from stim_experiments.utilities import KET_ONE_DENSITY_MATRIX, KET_ZERO_DENSITY_MATRIX
from tests.error_correcting_codes.generic_stabilizer_code.expected_states_generic_5_qubit import \
    ExpectedStatesGenericFiveQubit
from tests.error_correcting_codes.generic_stabilizer_code.expected_states_generic_steane import \
    ExpectedStatesGenericSteane
from tests.error_correcting_codes.generic_stabilizer_code.utilities import get_check_matrix_values_4_qubit, \
    get_check_matrix_values_5_qubit, \
    get_check_matrix_values_steane
from tests.utilities import states_are_equal


class TestGenericStabilizerCodeGeneralStabilizer:
    def test_input_state_must_be_size_of_logical_qubits_for_code(self):
        code_that_encodes_two_logical_bits = get_check_matrix_values_4_qubit()
        logical_qubit_state_of_only_one_qubit = KET_ZERO_DENSITY_MATRIX
        code = GenericStabilizerCode(generators=code_that_encodes_two_logical_bits,
                                     initial_logical_qubit_state=logical_qubit_state_of_only_one_qubit)
        with pytest.raises(ValueError, match="These generators encode 2 logical qubits, but an initial state of 1 was given."):
            code.encode_logical_qubit()
