import pytest
from cirq import Circuit, I, LineQubit, Simulator, X

from stim_experiments.error_correcting_codes.support.cat_state_creator.cat_state_creator_flag_pattern import \
    CatStateCreatorFlagPattern
from stim_experiments.utilities import FreshAncillasPool, TYPE_STATE_VECTOR, get_ket_cat_state_vector
from tests.error_correcting_codes.support.cat_state_creator.utilities import circuit_results_in_expected_state


class TestCatStateCreatorFlagPattern12Qubits:
    _num_qubits = 12
    _qubits = LineQubit.range(_num_qubits)
    _control_qubit = _qubits[0]

    @pytest.fixture(autouse=True, scope='class')
    def _setup(self):
        FreshAncillasPool().set_first_ancilla_num(first_ancilla_num=self._num_qubits)

    def test_no_errors(self):
        qubits = LineQubit.range(self._num_qubits)
        circuit = CatStateCreatorFlagPattern(qubit_register=qubits).get_cat_state_circuit()

        expected_state = get_ket_cat_state_vector(num_qubits=self._num_qubits)
        assert circuit_results_in_expected_state(circuit=circuit, expected_state=expected_state)

    @pytest.mark.parametrize('num_qubits_with_error', [3, 6, 9, 12])
    def test_x_error_on_multiple_of_3(self, num_qubits_with_error: int):
        assert self._run_multiple_of_3_qubits_affected(first_error_qubit_index=num_qubits_with_error - 1)

    def _run_multiple_of_3_qubits_affected(self, first_error_qubit_index: int) -> bool:
        circuit = self._get_circuit_with_x_error_on_first_n_qubits(n=first_error_qubit_index)
        expected_state = get_ket_cat_state_vector(num_qubits=self._num_qubits)
        return circuit_results_in_expected_state(circuit=circuit, expected_state=expected_state)

    def test_x_error_on_one_less_than_multiple_of_3_creates_error_on_multiple_of_3(self):
        multiple_of_3_index = 2
        circuit = self._get_circuit_with_x_error_on_first_n_qubits(n=multiple_of_3_index - 1)
        expected_state = self._get_cat_state_with_x_error(qubit_index_with_error=multiple_of_3_index)
        assert circuit_results_in_expected_state(circuit=circuit, expected_state=expected_state)

    def test_x_error_on_one_more_than_multiple_of_3(self):
        multiple_of_3_index = 2
        circuit = self._get_circuit_with_x_error_on_first_n_qubits(n=multiple_of_3_index + 1)
        expected_state = self._get_cat_state_with_x_error(qubit_index_with_error=multiple_of_3_index + 1)
        assert circuit_results_in_expected_state(circuit=circuit, expected_state=expected_state)

    def _get_circuit_with_x_error_on_first_n_qubits(self, n: int):
        first_error_qubit = self._qubits[n]
        circuit = CatStateCreatorFlagPattern(qubit_register=self._qubits).get_cat_state_circuit()
        faulty_moment = next(i for i, moment in enumerate(circuit.moments) if first_error_qubit in moment.qubits)
        circuit.insert(faulty_moment, X(self._control_qubit))
        return circuit

    def _get_cat_state_with_x_error(self, qubit_index_with_error) -> TYPE_STATE_VECTOR:
        ideal_state = get_ket_cat_state_vector(num_qubits=self._num_qubits)
        circuit = Circuit(
            [I(LineQubit(i)) for i in range(self._num_qubits)],
            X(LineQubit(qubit_index_with_error))
        )
        return Simulator().simulate(circuit, initial_state=ideal_state).final_state_vector
