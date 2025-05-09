from cirq import Circuit, Simulator, StateVectorTrialResult

from stim_experiments.utilities import TYPE_STATE_VECTOR, trace_out_ancillas_in_zero_state
from tests.utilities import states_are_equal


def circuit_results_in_expected_state(circuit: Circuit, expected_state: TYPE_STATE_VECTOR) -> bool:
    simulation: StateVectorTrialResult = Simulator().simulate(circuit)
    data_state = trace_out_ancillas_in_zero_state(state=simulation.final_state_vector, num_ancillas=1)
    return states_are_equal(data_state, expected_state)
