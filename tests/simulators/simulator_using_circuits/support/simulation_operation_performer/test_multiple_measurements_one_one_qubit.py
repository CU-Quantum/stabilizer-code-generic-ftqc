from functools import cached_property

import numpy

from stim_experiments.error_correcting_codes.generic_stabilizer_code.custom_dataclasses.state_and_measurements import \
    StateAndMeasurements
from stim_experiments.simulators.simulator_using_circuits.custom_dataclasses.simulation_operation import \
    ControlEncoding, SimulationOperation
from stim_experiments.simulators.simulator_using_circuits.support.simulation_operation_performer import \
    SimulationOperationPerformer
from stim_experiments.utilities import KET_ONE_STATE_VECTOR, KET_ZERO_STATE_VECTOR
from tests.simulators.simulator_using_circuits.support.simulation_operation_performer.error_correcting_code_stub import \
    ErrorCorrectingCodeStub


class TestMultipleMeasurementsOneOneQubit:
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
        performer = SimulationOperationPerformer(
            operation=self._measurement_operation_on_first_qubit,
            current_state=state_and_measurements,
            qubits=self._control_code.all_qubits
        )
        return performer.perform_operation()

    @property
    def _measurement_operation_on_first_qubit(self) -> SimulationOperation:
        return SimulationOperation(
            control_encoding=ControlEncoding(
                encoding=self._control_code,
                qubit_index=0
            )
        )

    @cached_property
    def _control_code(self) -> ErrorCorrectingCodeStub:
        return ErrorCorrectingCodeStub()
