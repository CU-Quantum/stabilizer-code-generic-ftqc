from cirq import LineQubit, Simulator, StateVectorTrialResult, X

from stim_experiments.error_correcting_codes.support.cat_state_creator.cat_state_creator_flag_pattern import \
    CatStateCreatorFlagPattern
from stim_experiments.utilities import FreshAncillasPool, get_ket_cat_state_vector, trace_out_ancillas_in_zero_state
from tests.utilities import states_are_equal


class TestCatStateCreatorFlagPattern12Qubits:
    def test_no_errors(self):
        num_qubits = 12
        qubits = LineQubit.range(num_qubits)
        circuit = CatStateCreatorFlagPattern(qubit_register=qubits).get_cat_state_circuit()

        simulation: StateVectorTrialResult = Simulator().simulate(circuit)
        expected_state = get_ket_cat_state_vector(num_qubits=num_qubits)
        assert states_are_equal(simulation.final_state_vector, expected_state)

    def test_x_error_on_first_3_qubits(self):
        num_qubits = 12
        qubits = LineQubit.range(num_qubits)
        control_qubit = qubits[0]
        first_error_qubit = qubits[2]

        FreshAncillasPool().set_first_ancilla_num(first_ancilla_num=num_qubits)
        circuit = CatStateCreatorFlagPattern(qubit_register=qubits).get_cat_state_circuit()
        faulty_moment = next(i for i, moment in enumerate(circuit.moments) if first_error_qubit in moment.qubits)
        circuit.insert(faulty_moment, X(control_qubit))

        simulation: StateVectorTrialResult = Simulator().simulate(circuit)
        data_state = trace_out_ancillas_in_zero_state(state=simulation.final_state_vector, num_ancillas=1)
        expected_state = get_ket_cat_state_vector(num_qubits=num_qubits)
        assert states_are_equal(data_state, expected_state)
