import numpy
import pytest
from cirq import LineQubit

from stim_experiments.error_correcting_codes.error_correcting_code.error_correcting_code import ErrorCorrectingCode
from stim_experiments.error_correcting_codes.generic_stabilizer_code.custom_dataclasses.state_and_measurements import \
    StateAndMeasurements
from stim_experiments.simulators.simulator_using_circuits.custom_dataclasses.simulation_operation import \
    LogicalEncodingIndex, SimulationOperation
from stim_experiments.simulators.simulator_using_circuits.support.simulation_operations_simulator.simulation_operation_simulator import \
    SimulationOperationSimulator
from stim_experiments.utilities import KET_ONE_STATE_VECTOR, KET_ZERO_STATE_VECTOR, tensor
from tests.simulators.simulator_using_circuits.support.simulation_operation_simulator.error_correcting_code_stub import \
    ErrorCorrectingCodeStub


class TestMultiqubitMeasurements:
    @pytest.fixture(autouse=True)
    def _setup(self):
        self._encodings = [
            ErrorCorrectingCodeStub(),
            ErrorCorrectingCodeStub(qubit_start_index=1)
        ]
        self._qubits = [qubit for encoding in self._encodings for qubit in encoding.all_qubits]

    def test_can_measure_multiple_qubits(self):
        numpy.random.seed(0)

        initial_state = tensor(KET_ZERO_STATE_VECTOR, KET_ONE_STATE_VECTOR)
        result = StateAndMeasurements(
            state=initial_state,
        )
        result = self._perform_measurement(encoding=self._encodings[0], state_and_measurements=result)
        result = self._perform_measurement(encoding=self._encodings[1], state_and_measurements=result)
        result = self._perform_measurement(encoding=self._encodings[0], state_and_measurements=result)

        assert result == StateAndMeasurements(
            state=initial_state,
            measurements={0: [0, 0], 1: [1]}
        )

    def _perform_measurement(self, encoding: ErrorCorrectingCode, state_and_measurements: StateAndMeasurements) -> StateAndMeasurements:
        operation = SimulationOperation(
            control_encoding=LogicalEncodingIndex(
                encoding=encoding,
                qubit_index_relative=0
            )
        )
        simulator = SimulationOperationSimulator(
            simulation_operation=operation,
            initial_state=state_and_measurements,
            qubits=self._qubits,
            control_ancilla=LineQubit(len(self._qubits))
        )
        return simulator.simulate_circuit()
