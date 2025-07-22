from cirq import Circuit, I, LineQubit
from numpy import sqrt

from stim_experiments.error_correcting_codes.support.cat_state_creator.cat_state_creator_cx_from_first_qubit import \
    CatStateCreatorCxFromFirstQubit
from stim_experiments.globals.fresh_ancillas_pool import FreshAncillasPool
from stim_experiments.simulations.error_correcting_simulator import get_error_correcting_simulator
from stim_experiments.utilities.utilities import KET_ONE_STATE_VECTOR, KET_PLUS_STATE_VECTOR, KET_ZERO_STATE_VECTOR, \
    states_are_equal, tensor


class TestCatStateCreatorCxFromFirstQubit:
    def test_create_no_qubits(self):
        creator = CatStateCreatorCxFromFirstQubit(qubit_register=[])
        circuit = Circuit(
            I(LineQubit(0)),
            creator.get_cat_state_circuit()
        )

        initial_state = KET_ZERO_STATE_VECTOR
        error_correcting_code_utilities = get_error_correcting_simulator(state=initial_state)
        state = error_correcting_code_utilities.get_state_after_circuit(circuit=circuit,
                                                                        num_data_qubits=1,
                                                                        initial_data_state=initial_state)
        assert states_are_equal(state.state, initial_state)

    def test_create_one_qubit_cat_state(self):
        qubits = LineQubit.range(1)
        creator = CatStateCreatorCxFromFirstQubit(qubit_register=qubits)
        circuit = creator.get_cat_state_circuit()

        initial_state = KET_ZERO_STATE_VECTOR
        error_correcting_code_utilities = get_error_correcting_simulator(state=initial_state)
        state = error_correcting_code_utilities.get_state_after_circuit(circuit=circuit,
                                                                        num_data_qubits=len(qubits),
                                                                        initial_data_state=initial_state)
        assert states_are_equal(state.state, KET_PLUS_STATE_VECTOR)

    def test_create_two_qubit_cat_state(self):
        qubits = LineQubit.range(2)
        FreshAncillasPool().set_first_ancilla_num(len(qubits))
        creator = CatStateCreatorCxFromFirstQubit(qubit_register=qubits)
        circuit = creator.get_cat_state_circuit()

        initial_state = tensor(KET_ZERO_STATE_VECTOR, KET_ZERO_STATE_VECTOR)
        error_correcting_code_utilities = get_error_correcting_simulator(state=initial_state)
        state = error_correcting_code_utilities.get_state_after_circuit(circuit=circuit,
                                                                        num_data_qubits=len(qubits),
                                                                        initial_data_state=initial_state)
        expected_state = (1 / sqrt(2)) * (tensor(KET_ZERO_STATE_VECTOR, KET_ZERO_STATE_VECTOR)
                                          + tensor(KET_ONE_STATE_VECTOR, KET_ONE_STATE_VECTOR))
        assert states_are_equal(state.state, expected_state)
