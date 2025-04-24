from cirq import Circuit, H, LineQubit, X
from numpy import sqrt

from stim_experiments.error_correcting_codes.error_correcting_code_utilities import get_error_correcting_code_utilities
from stim_experiments.utilities import KET_ONE_STATE_VECTOR, KET_PLUS_STATE_VECTOR, KET_ZERO_STATE_VECTOR, tensor
from tests.utilities import states_are_equal


class CatStateCircuitCreator:
    def __init__(self, target_qubits: list[LineQubit] = None):
        self._target_qubits = target_qubits

    def create_circuit(self) -> Circuit:
        if not self._target_qubits:
            return Circuit()
        return Circuit(
            H(self._target_qubits[0]),
            [X(self._target_qubits[i]).controlled_by(self._target_qubits[i - 1]) for i in range(1, len(self._target_qubits))]
        )


class TestCatStateCircuitCreator:
    def test_create_no_qubits(self):
        creator = CatStateCircuitCreator(target_qubits=[])
        circuit = creator.create_circuit()

        initial_state = KET_ZERO_STATE_VECTOR
        error_correcting_code_utilities = get_error_correcting_code_utilities(state=initial_state)
        state = error_correcting_code_utilities.get_state_after_circuit(circuit=circuit,
                                                                        initial_state=initial_state,
                                                                        qubit_order=[LineQubit(0)],)
        assert states_are_equal(state.state, initial_state)

    def test_create_one_qubit_cat_state(self):
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
