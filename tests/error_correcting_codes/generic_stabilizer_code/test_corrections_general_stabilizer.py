import pytest
from cirq import X, Y, Z

from stim_experiments.error_correcting_codes.generic_stabilizer_code.generic_stabilizer_code import \
    GenericStabilizerCode
from stim_experiments.utilities import KET_ZERO_DENSITY_MATRIX
from tests.error_correcting_codes.corrections_test_helper import CorrectionsTestHelper
from tests.error_correcting_codes.generic_stabilizer_code.expected_states_generic_5_qubit import \
    ExpectedStatesGenericFiveQubit
from tests.error_correcting_codes.generic_stabilizer_code.utilities import get_check_matrix_values_5_qubit


class TestCorrectionsFiveQubit:
    _all_qubits = range(5)

    @pytest.fixture(autouse=True)
    def _setup(self):
        code = GenericStabilizerCode(generators=get_check_matrix_values_5_qubit(), initial_logical_qubit_state=KET_ZERO_DENSITY_MATRIX)
        self._helper = CorrectionsTestHelper(expected_states_utilities=ExpectedStatesGenericFiveQubit(), code=code)

    @pytest.mark.parametrize('qubit_index', _all_qubits)
    def test_bit_flip_error_is_correctly_applied(self, qubit_index: int):
        assert self._helper.state_matches_expected_after_error(error_gate=X, qubit_index=qubit_index)

    @pytest.mark.parametrize('qubit_index', _all_qubits)
    def test_phase_flip_error_is_correctly_applied(self, qubit_index: int):
        assert self._helper.state_matches_expected_after_error(error_gate=Z, qubit_index=qubit_index)

    @pytest.mark.parametrize('qubit_index', _all_qubits)
    def test_pauli_y_error_is_correctly_applied(self, qubit_index: int):
        assert self._helper.state_matches_expected_after_error(error_gate=Y, qubit_index=qubit_index)

    @pytest.mark.parametrize('qubit_index', _all_qubits)
    def test_bit_flip_error_is_corrected(self, qubit_index: int):
        assert self._helper.error_is_corrected(error_gate=X, qubit_index=qubit_index)

    @pytest.mark.parametrize('qubit_index', _all_qubits)
    def test_phase_flip_error_is_corrected(self, qubit_index: int):
        assert self._helper.error_is_corrected(error_gate=Z, qubit_index=qubit_index)

    @pytest.mark.parametrize('qubit_index', _all_qubits)
    def test_pauli_y_error_is_corrected(self, qubit_index: int):
        self._helper.error_is_corrected(error_gate=Y, qubit_index=qubit_index)
