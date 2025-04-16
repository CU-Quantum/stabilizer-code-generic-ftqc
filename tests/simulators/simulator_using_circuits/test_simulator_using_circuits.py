import pytest
from numpy import array

from stim_experiments.error_correcting_codes.error_correcting_code.error_correcting_code import ErrorCorrectingCode
from stim_experiments.custom_dataclasses.logical_operation import LogicalOperation
from stim_experiments.simulators.custom_dataclasses.simulator_result import SimulatorResult
from stim_experiments.simulators.simulator_using_circuits.simulator_using_circuits import SimulatorUsingCircuits


class CodeStub(ErrorCorrectingCode):
    def __init__(self):
        super().__init__(num_data_qubits=0, num_ancilla_qubits=0)

    def _encode_logical_qubit(self) -> None:
        pass

    def correct_errors(self) -> None:
        pass

    def apply_operation(self, operation: LogicalOperation) -> None:
        pass


@pytest.mark.skip("Not implemented")
class TestSimulatorCircuit:
    def test_trivial(self):
        code = CodeStub()
        simulator = SimulatorUsingCircuits(error_correcting_code=code)
        operations = []
        result = simulator.simulate(operations=operations)
        assert result == SimulatorResult(
            state=array([[]]),
            measurements={},
        )

    # def test_logical_x(self):
    #     code = GenericStabilizerCode(generators=get_check_matrix_values_5_qubit())
    #     simulator = SimulatorUsingCircuits(error_correcting_code=code)
    #     operations = [LogicalOperation(gate=LogicalGateLabel.X, qubit_index=0)]
    #     result = simulator.simulate(operations=operations)
    #     assert result == SimulatorResult(
    #         state=ExpectedStatesGenericFiveQubit().get_logical_one_density_matrix(),
    #         measurements={},
    #     )
    #
    #
    # def test_logical_z(self):
    #     code = GenericStabilizerCode(generators=get_check_matrix_values_5_qubit(), initial_logical_qubit_state_density_matrix=KET_ONE_DENSITY_MATRIX)
    #     simulator = SimulatorUsingCircuits(error_correcting_code=code)
    #     operations = [LogicalOperation(gate=LogicalGateLabel.Z, qubit_index=0)]
    #     result = simulator.simulate(operations=operations)
    #     assert result == SimulatorResult(
    #         state=ExpectedStatesGenericFiveQubit().get_logical_one_density_matrix(),
    #         measurements={},
    #     )
