import numpy.random
import pytest
from cirq import LineQubit

from stim_experiments.custom_dataclasses.logical_operation import LogicalGateLabel, LogicalOperation
from stim_experiments.custom_dataclasses.state_and_measurements import \
    StateAndMeasurements
from stim_experiments.simulators.simulator_using_circuits.custom_dataclasses.simulation_operation import \
    LogicalEncodingIndex, SimulationOperation, TargetEncoding
from stim_experiments.simulators.simulator_using_circuits.support.simulation_operations_simulator.simulation_operation_simulator import \
    SimulationOperationSimulator
from stim_experiments.utilities.utilities import KET_ONE_STATE_VECTOR, KET_ZERO_STATE_VECTOR, \
    TYPE_STATE_VECTOR_OR_DENSITY_MATRIX, tensor
from tests.simulators.simulator_using_circuits.support.simulation_operation_simulator.error_correcting_code_stub import \
    ErrorCorrectingCodeStub


class TestSimulationOperationSimulator:
    def test_blank_simulation_operation(self):
        operation = SimulationOperation()
        with pytest.raises(ValueError, match="Was given a SimulationOperation with no encoding."):
            simulator = SimulationOperationSimulator(simulation_operation=operation,
                                                     initial_state=KET_ZERO_STATE_VECTOR,
                                                     qubits=[],
                                                     control_ancilla=LineQubit(0),)
            simulator.simulate_circuit()

    def test_target_operation_only(self):
        code = ErrorCorrectingCodeStub()
        operation = SimulationOperation(
            target_encoding=TargetEncoding(
                operation=LogicalOperation(
                    LogicalGateLabel.X,
                    qubit_index=0
                ),
                encoding=code,
            )
        )
        simulator = SimulationOperationSimulator(simulation_operation=operation,
                                                 initial_state=StateAndMeasurements(state=KET_ZERO_STATE_VECTOR),
                                                 qubits=code.all_qubits,
                                                 control_ancilla=LineQubit(len(code.all_qubits)))
        result = simulator.simulate_circuit()

        assert result == StateAndMeasurements(
            state=KET_ONE_STATE_VECTOR,
            measurements={},
        )

    @pytest.mark.parametrize(['initial_coded_state', 'expected_coded_state'], [
        (tensor(KET_ZERO_STATE_VECTOR, KET_ONE_STATE_VECTOR), tensor(KET_ONE_STATE_VECTOR, KET_ONE_STATE_VECTOR)),
        (tensor(KET_ZERO_STATE_VECTOR, KET_ZERO_STATE_VECTOR), tensor(KET_ZERO_STATE_VECTOR, KET_ZERO_STATE_VECTOR)),
    ])
    def test_target_operation_with_control(self, initial_coded_state: TYPE_STATE_VECTOR_OR_DENSITY_MATRIX, expected_coded_state: TYPE_STATE_VECTOR_OR_DENSITY_MATRIX):
        target_code = ErrorCorrectingCodeStub()
        control_code = ErrorCorrectingCodeStub(qubit_start_index=1)
        operation = SimulationOperation(
            target_encoding=TargetEncoding(
                operation=LogicalOperation(
                    LogicalGateLabel.X,
                    qubit_index=0
                ),
                encoding=target_code,
            ),
            control_encoding=LogicalEncodingIndex(
                encoding=control_code,
                qubit_index_relative=0,
                qubit_index_logical=1
            )
        )

        simulator = SimulationOperationSimulator(simulation_operation=operation,
                                                 initial_state=StateAndMeasurements(initial_coded_state),
                                                 qubits=target_code.all_qubits + control_code.all_qubits,
                                                 control_ancilla=LineQubit(len(target_code.all_qubits + control_code.all_qubits)))
        result = simulator.simulate_circuit()

        assert result == StateAndMeasurements(
            state=expected_coded_state,
            measurements={},
        )

    @pytest.mark.parametrize(['initial_coded_state', 'expected_measurement'], [
        (KET_ZERO_STATE_VECTOR, 0),
        (KET_ONE_STATE_VECTOR, 1),
    ])
    def test_measurement_operation(self, initial_coded_state: TYPE_STATE_VECTOR_OR_DENSITY_MATRIX, expected_measurement: int):
        numpy.random.seed(0)
        num_trials = 5
        for _ in range(num_trials):
            control_code = ErrorCorrectingCodeStub()
            operation = SimulationOperation(
                control_encoding=LogicalEncodingIndex(
                    encoding=control_code,
                    qubit_index_relative=0
                )
            )
            simulator = SimulationOperationSimulator(simulation_operation=operation,
                                                     initial_state=StateAndMeasurements(initial_coded_state),
                                                     qubits=control_code.all_qubits,
                                                     control_ancilla=LineQubit(len(control_code.all_qubits)))
            result = simulator.simulate_circuit()

            assert result == StateAndMeasurements(
                state=initial_coded_state,
                measurements={0: [expected_measurement]},
            )

    def test_ancilla_qubit_in_provided_qubits(self):
        qubits = [LineQubit(0), LineQubit(1)]
        ancilla_qubit = qubits[1]
        code = ErrorCorrectingCodeStub()

        operation = SimulationOperation(
            target_encoding=TargetEncoding(
                operation=LogicalOperation(
                    LogicalGateLabel.X,
                    qubit_index=0
                ),
                encoding=code,
            )
        )

        initial_state = tensor(KET_ZERO_STATE_VECTOR, KET_ZERO_STATE_VECTOR)

        performer = SimulationOperationSimulator(
            simulation_operation=operation,
            initial_state=StateAndMeasurements(state=initial_state,),
            qubits=qubits,
            control_ancilla=ancilla_qubit
        )

        result = performer.simulate_circuit()

        expected_state = tensor(KET_ONE_STATE_VECTOR, KET_ZERO_STATE_VECTOR)
        assert result == StateAndMeasurements(
            state=expected_state,
            measurements={},
        )
