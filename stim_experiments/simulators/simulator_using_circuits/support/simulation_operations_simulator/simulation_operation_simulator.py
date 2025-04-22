from copy import deepcopy
from functools import cached_property

from cirq import Circuit, LineQubit

from stim_experiments.error_correcting_codes.generic_stabilizer_code.custom_dataclasses.state_and_measurements import \
    StateAndMeasurements
from stim_experiments.error_correcting_codes.error_correcting_code_utilities import get_error_correcting_code_utilities
from stim_experiments.simulators.simulator_using_circuits.custom_dataclasses.simulation_operation import \
    SimulationOperation
from stim_experiments.simulators.simulator_using_circuits.support.simulation_operations_simulator.support.circuit_from_operation_creator import \
    CircuitFromOperationCreator
from stim_experiments.utilities import tensor, trace_out_ancillas_in_zero_state


class SimulationOperationSimulator:
    def __init__(self,
                 simulation_operation: SimulationOperation,
                 initial_state: StateAndMeasurements,
                 qubits: list[LineQubit],
                 control_ancilla: LineQubit):
        self._simulation_operation = simulation_operation
        self.initial_state = initial_state
        self._qubits = qubits
        self._control_ancilla = control_ancilla

    def simulate_circuit(self) -> StateAndMeasurements:
        circuit = CircuitFromOperationCreator(operation=self._simulation_operation, control_ancilla=self._control_ancilla).create_circuit()
        result = self._run_simulation(circuit=circuit)
        return StateAndMeasurements(
            state=result.state,
            measurements=self._combine_measurements(new_measurements=result.measurements),
        )

    def _run_simulation(self, circuit: Circuit) -> StateAndMeasurements:
        error_correcting_code_utilities = get_error_correcting_code_utilities(state=self.initial_state.state)
        if self._control_ancilla in self._qubits:
            return error_correcting_code_utilities.get_state_after_circuit(circuit=circuit,
                                                                           qubit_order=self._qubits,
                                                                           initial_state=self.initial_state.state)
        else:
            ancilla_state = error_correcting_code_utilities.zero_state
            state = tensor(self.initial_state.state, ancilla_state)
            simulated_state_and_measurements = error_correcting_code_utilities.get_state_after_circuit(
                circuit=circuit,
                qubit_order=self._qubits + [self._control_ancilla],
                initial_state=state)
            return StateAndMeasurements(
                state=trace_out_ancillas_in_zero_state(simulated_state_and_measurements.state, num_ancillas=1),
                measurements=simulated_state_and_measurements.measurements,
            )

    def _combine_measurements(self, new_measurements: dict[int, list[int]]) -> dict[int, list[int]]:
        if not new_measurements:
            return self.initial_state.measurements
        measurement_from_control_ancilla = list(new_measurements.values())[0][0]

        combined_measurements = deepcopy(self.initial_state.measurements)
        combined_measurements[self._logical_qubit_measurement_index].append(measurement_from_control_ancilla)
        return combined_measurements

    @cached_property
    def _logical_qubit_measurement_index(self):
        local_qubit_index = self._simulation_operation.control_encoding.qubit_index
        first_qubit_x = self._simulation_operation.control_encoding.encoding.all_qubits[0].x
        global_qubit_index = first_qubit_x + local_qubit_index
        return global_qubit_index
