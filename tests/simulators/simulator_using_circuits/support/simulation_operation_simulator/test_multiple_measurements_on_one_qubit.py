from functools import cached_property

import numpy
import pytest
from cirq import LineQubit

from stim_experiments.error_correcting_codes.generic_stabilizer_code.custom_dataclasses.state_and_measurements import \
    StateAndMeasurements
from stim_experiments.simulators.simulator_using_circuits.custom_dataclasses.simulation_operation import \
    LogicalEncodingIndex, SimulationOperation
from stim_experiments.simulators.simulator_using_circuits.support.simulation_operations_simulator.simulation_operation_simulator import \
    SimulationOperationSimulator
from stim_experiments.utilities import KET_ONE_STATE_VECTOR, KET_ZERO_STATE_VECTOR
from tests.simulators.simulator_using_circuits.support.simulation_operation_simulator.error_correcting_code_stub import \
    ErrorCorrectingCodeStub


class TestMultipleMeasurementsOnOneQubit:
    @pytest.fixture(autouse=True)
    def _setup(self):
        self._control_code = ErrorCorrectingCodeStub()

    def test_multiple_measurements_on_same_qubit_combines_results(self):
        arbitrary_seed = 0
        numpy.random.seed(arbitrary_seed)

        zero_state_with_no_measurements = StateAndMeasurements(
            state=KET_ZERO_STATE_VECTOR,
        )
        result = self._perform_measurement_on_first_qubit(state_and_measurements=zero_state_with_no_measurements)

        one_state_with_previous_measurements = StateAndMeasurements(
            state=KET_ONE_STATE_VECTOR,
            measurements=result.measurements
        )
        result = self._perform_measurement_on_first_qubit(state_and_measurements=one_state_with_previous_measurements)

        assert result == StateAndMeasurements(
            state=KET_ONE_STATE_VECTOR,
            measurements={0: [0, 1]}
        )

    def _perform_measurement_on_first_qubit(self, state_and_measurements: StateAndMeasurements) -> StateAndMeasurements:
        simulator = SimulationOperationSimulator(
            simulation_operation=self._measurement_operation_on_first_qubit,
            initial_state=state_and_measurements,
            qubits=self._control_code.all_qubits,
            control_ancilla=LineQubit(len(self._control_code.all_qubits)),
        )
        return simulator.simulate_circuit()

    @property
    def _measurement_operation_on_first_qubit(self) -> SimulationOperation:
        return SimulationOperation(
            control_encoding=LogicalEncodingIndex(
                encoding=self._control_code,
                qubit_index_relative=0
            )
        )
