import pytest
from cirq import LineQubit

from stim_experiments.error_correcting_codes.support.cat_state_creator.cat_state_creator_flag_pattern import \
    CatStateCreatorFlagPattern
from stim_experiments.utilities import FreshAncillasPool, get_ket_cat_state_vector
from tests.error_correcting_codes.support.cat_state_creator.utilities import circuit_results_in_expected_state, \
    get_cat_state_with_x_error, get_circuit_with_x_error_on_first_n_qubits


class TestCatStateCreatorFlagPatternLessThanPerfectNumberOfQubits:
    @pytest.fixture(autouse=True, scope='class')
    def _setup(self):
        FreshAncillasPool().set_first_ancilla_num(first_ancilla_num=11)

    def test_one_fewer_qubit_no_errors(self):
        perfect_size = 12
        target_size = perfect_size - 1
        qubits = LineQubit.range(target_size)
        circuit = CatStateCreatorFlagPattern(qubit_register=qubits).get_cat_state_circuit()
        expected_state = get_ket_cat_state_vector(num_qubits=target_size)
        assert circuit_results_in_expected_state(circuit=circuit, expected_state=expected_state)

    def test_one_fewer_qubit_x_errors_on_all_qubits_except_last_two(self):
        perfect_size = 12
        target_size = perfect_size - 1
        qubits = LineQubit.range(target_size)
        circuit = get_circuit_with_x_error_on_first_n_qubits(qubits=qubits, n=target_size - 2)
        expected_state = get_ket_cat_state_vector(num_qubits=target_size)
        assert circuit_results_in_expected_state(circuit=circuit, expected_state=expected_state)

    def test_one_fewer_qubit_x_error_on_all_qubits_except_last_three(self):
        perfect_size = 12
        target_size = perfect_size - 1
        qubits = LineQubit.range(target_size)
        circuit = get_circuit_with_x_error_on_first_n_qubits(qubits=qubits, n=target_size - 3)
        expected_state = get_cat_state_with_x_error(num_qubits=target_size, qubit_index_with_error=target_size - 3)
        assert circuit_results_in_expected_state(circuit=circuit, expected_state=expected_state)

    def test_two_fewer_qubit_no_errors(self):
        perfect_size = 12
        target_size = perfect_size - 2
        qubits = LineQubit.range(target_size)
        circuit = CatStateCreatorFlagPattern(qubit_register=qubits).get_cat_state_circuit()
        expected_state = get_ket_cat_state_vector(num_qubits=target_size)
        assert circuit_results_in_expected_state(circuit=circuit, expected_state=expected_state)

    def test_two_fewer_qubits_x_error_on_all_qubits_except_last_two(self):
        perfect_size = 12
        target_size = perfect_size - 2
        qubits = LineQubit.range(target_size)
        circuit = get_circuit_with_x_error_on_first_n_qubits(qubits=qubits, n=target_size - 2)
        expected_state = get_ket_cat_state_vector(num_qubits=target_size)
        assert circuit_results_in_expected_state(circuit=circuit, expected_state=expected_state)
