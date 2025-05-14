from cirq import Circuit, LineQubit, Simulator, StateVectorTrialResult

from stim_experiments.error_correcting_codes.support.cat_state_creator.cat_state_creator_flag_pattern.cat_state_creator_flag_pattern import \
    CatStateCreatorFlagPattern
from stim_experiments.utilities import KET_PLUS_STATE_VECTOR, get_ket_cat_state_vector
from tests.error_correcting_codes.support.cat_state_creator.utilities import circuit_results_in_expected_state
from tests.utilities import states_are_equal


class TestCatStateCreatorFlagPattern:
    def test_trivial(self):
        qubits = LineQubit.range(0)
        circuit = CatStateCreatorFlagPattern(qubit_register=qubits).get_cat_state_circuit()
        assert circuit == Circuit()

    def test_single_qubit(self):
        qubits = LineQubit.range(1)
        circuit = CatStateCreatorFlagPattern(qubit_register=qubits).get_cat_state_circuit()
        assert circuit_results_in_expected_state(circuit=circuit, expected_state=KET_PLUS_STATE_VECTOR)

    def test_three_qubits(self):
        num_qubits = 3
        qubits = LineQubit.range(num_qubits)
        circuit = CatStateCreatorFlagPattern(qubit_register=qubits).get_cat_state_circuit()
        expected_state = get_ket_cat_state_vector(num_qubits=num_qubits)
        simulation: StateVectorTrialResult = Simulator().simulate(circuit)
        assert states_are_equal(simulation.final_state_vector, expected_state)
