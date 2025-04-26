from cirq import LineQubit
from numpy import sqrt

from stim_experiments.error_correcting_codes.error_correcting_code_utilities import get_error_correcting_code_utilities
from stim_experiments.utilities import KET_ONE_STATE_VECTOR, KET_PLUS_STATE_VECTOR, KET_ZERO_STATE_VECTOR, tensor
from tests.utilities import states_are_equal


class TestCatStateCircuitCreator:
    def test_create_no_qubits(self):
        assert False
        creator = CatStateCircuitCreator(target_qubits=[])
        circuit = creator.create_circuit()

        initial_state = KET_ZERO_STATE_VECTOR
        error_correcting_code_utilities = get_error_correcting_code_utilities(state=initial_state)
        state = error_correcting_code_utilities.get_state_after_circuit(circuit=circuit,
                                                                        initial_state=initial_state,
                                                                        qubit_order=[LineQubit(0)],)
        assert states_are_equal(state.state, initial_state)

    def test_create_one_qubit_cat_state(self):
        assert False
        qubits = LineQubit.range(1)
        creator = CatStateCircuitCreator(target_qubits=qubits)
        circuit = creator.create_circuit()

        initial_state = KET_ZERO_STATE_VECTOR
        error_correcting_code_utilities = get_error_correcting_code_utilities(state=initial_state)
        state = error_correcting_code_utilities.get_state_after_circuit(circuit=circuit,
                                                                        initial_state=initial_state,
                                                                        qubit_order=qubits,)
        assert states_are_equal(state.state, KET_PLUS_STATE_VECTOR)

    def test_create_two_qubit_cat_state(self):
        assert False
        qubits = LineQubit.range(2)
        creator = CatStateCircuitCreator(target_qubits=qubits)
        circuit = creator.create_circuit()

        initial_state = tensor(KET_ZERO_STATE_VECTOR, KET_ZERO_STATE_VECTOR)
        error_correcting_code_utilities = get_error_correcting_code_utilities(state=initial_state)
        state = error_correcting_code_utilities.get_state_after_circuit(circuit=circuit,
                                                                        initial_state=initial_state,
                                                                        qubit_order=qubits,)
        expected_state = (1 / sqrt(2)) * (tensor(KET_ZERO_STATE_VECTOR, KET_ZERO_STATE_VECTOR)
                                          + tensor(KET_ONE_STATE_VECTOR, KET_ONE_STATE_VECTOR))
        assert states_are_equal(state.state, expected_state)
