from cirq import dirac_notation
from numpy import array

from stim_experiments.error_correcting_codes.generic_stabilizer_code.generic_stabilizer_code import \
    GenericStabilizerCode
from stim_experiments.simulators.custom_dataclasses.logical_operation import LogicalGateLabel, \
    LogicalOperation
from stim_experiments.simulators.custom_dataclasses.simulator_result import SimulatorResult
from stim_experiments.simulators.simulator_using_circuits.simulator_using_circuits import SimulatorUsingCircuits
from tests.error_correcting_codes.generic_stabilizer_code.expected_states_generic_5_qubit import \
    ExpectedStatesGenericFiveQubit
from tests.error_correcting_codes.generic_stabilizer_code.utilities import get_check_matrix_values_4_qubit, \
    get_check_matrix_values_5_qubit
from tests.utilities import get_pure_state_from_density_matrix_of_only_pure_states


class TestSimulatorCircuit:
    def test_trivial(self):
        code = GenericStabilizerCode(generators=get_check_matrix_values_4_qubit())
        simulator = SimulatorUsingCircuits(error_correcting_code=code)
        operations = []
        result = simulator.simulate(operations=operations)
        assert result == SimulatorResult(
            state=array([[]]),
            measurements={},
        )

    def test_logical_not(self):
        code = GenericStabilizerCode(generators=get_check_matrix_values_5_qubit())
        simulator = SimulatorUsingCircuits(error_correcting_code=code)
        operations = [LogicalOperation(gate=LogicalGateLabel.X, qubit_indices=[0])]
        result = simulator.simulate(operations=operations)
        # result_ket = dirac_notation(get_pure_state_from_density_matrix_of_only_pure_states(density_matrix=result.state))
        # expected_ket = dirac_notation(get_pure_state_from_density_matrix_of_only_pure_states(density_matrix=ExpectedStatesGenericFiveQubit().get_logical_one_density_matrix()))
        assert result == SimulatorResult(
            state=ExpectedStatesGenericFiveQubit().get_logical_one_density_matrix(),
            measurements={},
        )
