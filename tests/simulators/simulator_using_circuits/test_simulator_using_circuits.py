from typing import List

from numpy import array

from stim_experiments.error_correcting_codes.error_correcting_code.error_correcting_code import ErrorCorrectingCode
from stim_experiments.custom_dataclasses.logical_operation import LogicalGateLabel, LogicalOperation
from stim_experiments.error_correcting_codes.generic_stabilizer_code.generic_stabilizer_code import \
    GenericStabilizerCode
from stim_experiments.error_correcting_codes.generic_stabilizer_code.support.stabilizer_transformer import \
    TransformationGate, TransformationOperation
from stim_experiments.simulators.custom_dataclasses.simulator_result import SimulatorResult
from stim_experiments.simulators.simulator_using_circuits.simulator_using_circuits import SimulatorUsingCircuits
from stim_experiments.utilities import KET_ONE_STATE_VECTOR
from tests.error_correcting_codes.generic_stabilizer_code.utilities import get_check_matrix_values_4_qubit, \
    get_check_matrix_values_5_qubit


class TestSimulatorCircuit:
    def test_trivial(self):
        code = GenericStabilizerCode(generators=get_check_matrix_values_5_qubit())
        simulator = SimulatorUsingCircuits(error_correcting_code=code, operations=[])
        result = simulator.simulate()
        assert result == SimulatorResult(
            encodings=[],
            measurements={},
        )

    def test_logical_x(self):
        code = GenericStabilizerCode(generators=get_check_matrix_values_5_qubit())
        operations = [TransformationOperation(gate=TransformationGate.X, target_qubit_index=0)]
        simulator = SimulatorUsingCircuits(error_correcting_code=code, operations=operations)
        result = simulator.simulate()
        assert result == SimulatorResult(
            encodings=[GenericStabilizerCode(generators=get_check_matrix_values_5_qubit(), initial_logical_qubit_state=KET_ONE_STATE_VECTOR)],
            measurements={},
        )

    # def test_logical_z(self):
    #     code = GenericStabilizerCode(generators=get_check_matrix_values_5_qubit(), initial_logical_qubit_state_density_matrix=KET_ONE_DENSITY_MATRIX)
    #     simulator = SimulatorUsingCircuits(error_correcting_code=code)
    #     operations = [LogicalOperation(gate=LogicalGateLabel.Z, qubit_index=0)]
    #     result = simulator.simulate(operations=operations)
    #     assert result == SimulatorResult(
    #         state=ExpectedStatesGenericFiveQubit().get_logical_one_density_matrix(),
    #         measurements={},
    #     )
