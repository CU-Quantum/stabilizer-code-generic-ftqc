import pytest
from cirq import LineQubit

from stim_experiments.error_correcting_codes.support.cat_state_creator.cat_state_creator_flag_pattern import \
    CatStateCreatorFlagPattern
from stim_experiments.utilities import FreshAncillasPool, get_ket_cat_state_vector
from tests.error_correcting_codes.support.cat_state_creator.utilities import circuit_results_in_expected_state


class TestCatStateCreatorFlagPatternLessThanPerfectNumberOfQubits:
    @pytest.fixture(autouse=True, scope='class')
    def _setup(self):
        FreshAncillasPool().set_first_ancilla_num(first_ancilla_num=11)

    def test_11_qubits_no_errors(self):
        perfect_size = 12
        target_size = perfect_size - 1
        qubits = LineQubit.range(target_size)
        circuit = CatStateCreatorFlagPattern(qubit_register=qubits).get_cat_state_circuit()
        expected_state = get_ket_cat_state_vector(num_qubits=target_size)
        assert circuit_results_in_expected_state(circuit=circuit, expected_state=expected_state)
