import pytest
from cirq import Circuit, X

from stim_experiments.error_correcting_codes.error_correcting_code_utilities import get_error_correcting_code_utilities
from stim_experiments.error_correcting_codes.support.universal_hadamard.universal_hadamard_fault_tolerant.support.three_cat_subregister_parity_code_to_computational_logical import \
    ThreeCatSubregisterParityCodeToComputationalLogical
from stim_experiments.error_correcting_codes.three_cat_subregister_parity_code.three_cat_subregister_parity_code import \
    ThreeCatSubregisterParityCode
from stim_experiments.globals.fresh_ancillas_pool import FreshAncillasPool
from stim_experiments.utilities.utilities import KET_MINUS_STATE_VECTOR, KET_PLUS_STATE_VECTOR, KET_ZERO_STATE_VECTOR, \
    TYPE_STATE_VECTOR, states_are_equal, tensor
from tests.error_correcting_codes.support.universal_hadamard.universal_hadamard_fault_tolerant.single_qubit_code import SingleQubitCode
from tests.utilities import set_configuration_to_reduce_ancilla_qubits


class TestUniversalHadamardCodeToComputationalLogical:

    @pytest.fixture(autouse=True)
    def _setup(self):
        arbitrary_desired_code = SingleQubitCode()
        self._three_cat_subregister_parity_code = ThreeCatSubregisterParityCode(num_qubits_in_cat_state=len(arbitrary_desired_code.data_qubits))
        self._num_data_qubits = len(self._three_cat_subregister_parity_code.data_qubits)
        self._helper = ThreeCatSubregisterParityCodeToComputationalLogical(
            three_cat_subregister_parity_code=self._three_cat_subregister_parity_code, desired_encoding=arbitrary_desired_code)
        FreshAncillasPool().set_first_ancilla_num(first_ancilla_num=self._num_data_qubits)
        set_configuration_to_reduce_ancilla_qubits()

    def test_puts_zero_into_plus(self):
        circuit = Circuit(
            self._three_cat_subregister_parity_code.encode_logical_qubit(),
            self._helper.get_circuit()
        )
        expected_state = tensor(KET_PLUS_STATE_VECTOR, KET_ZERO_STATE_VECTOR, KET_ZERO_STATE_VECTOR)
        assert self._circuit_results_in_expected_state(circuit=circuit, expected_state=expected_state)

    def test_puts_one_into_minus(self):
        circuit = Circuit(
            [X(qubit) for qubit in self._three_cat_subregister_parity_code.data_qubits],
            self._three_cat_subregister_parity_code.encode_logical_qubit(),
            self._helper.get_circuit()
        )
        expected_state = tensor(KET_MINUS_STATE_VECTOR, KET_ZERO_STATE_VECTOR, KET_ZERO_STATE_VECTOR)
        assert self._circuit_results_in_expected_state(circuit=circuit, expected_state=expected_state)

    def _circuit_results_in_expected_state(self, circuit: Circuit, expected_state: TYPE_STATE_VECTOR):
        utilities = get_error_correcting_code_utilities(state=expected_state)
        simulated_state = utilities.get_state_after_circuit(
            circuit=circuit,
            num_data_qubits=self._num_data_qubits,
        ).state
        return states_are_equal(simulated_state, expected_state)


