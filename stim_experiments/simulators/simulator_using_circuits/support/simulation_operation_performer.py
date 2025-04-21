from copy import deepcopy
from typing import List

from cirq import Circuit, H, LineQubit, M, R, kron
from proto.utils import cached_property

from stim_experiments.custom_dataclasses.logical_operation import LogicalGateLabel, LogicalOperation
from stim_experiments.error_correcting_codes.generic_stabilizer_code.error_correcting_code_utilities import \
    ErrorCorrectingCodeUtilities
from stim_experiments.error_correcting_codes.generic_stabilizer_code.custom_dataclasses.state_and_measurements import \
    StateAndMeasurements
from stim_experiments.error_correcting_codes.utilities import get_error_correcting_code_utilities
from stim_experiments.simulators.simulator_using_circuits.custom_dataclasses.simulation_operation import \
    SimulationOperation
from stim_experiments.utilities import trace_out_ancillas_in_zero_state


class SimulationOperationPerformer:
    def __init__(self,
                 operation: SimulationOperation,
                 current_state: StateAndMeasurements,
                 qubits: List[LineQubit],
                 ancilla_qubit: LineQubit):
        self._operation = operation
        self._current_state = current_state
        self._qubits = qubits
        self._ancilla_qubit = ancilla_qubit

    def perform_operation(self) -> StateAndMeasurements:
        circuit = self._get_circuit()
        result = self._run_simulation(circuit=circuit)
        combined_measurements = self._combine_measurements(new_measurements=result.measurements)

        return StateAndMeasurements(
            state=result.state,
            measurements=combined_measurements,
        )

    def _run_simulation(self, circuit: Circuit) -> StateAndMeasurements:
        if self._ancilla_qubit in self._qubits:
            return self._error_correcting_code_utilities.get_state_after_circuit(circuit=circuit,
                                                                                 qubit_order=self._qubits,
                                                                                 initial_state=self._current_state.state)
        else:
            ancilla_state = self._error_correcting_code_utilities.zero_state
            state = kron(self._current_state.state, ancilla_state, shape_len=len(self._current_state.state.shape))
            simulated_state_and_measurements = self._error_correcting_code_utilities.get_state_after_circuit(
                circuit=circuit,
                qubit_order=self._qubits + [self._ancilla_qubit],
                initial_state=state)
            return StateAndMeasurements(
                state=trace_out_ancillas_in_zero_state(simulated_state_and_measurements.state, num_ancillas=1),
                measurements=simulated_state_and_measurements.measurements,
            )

    def _combine_measurements(self, new_measurements: dict[int, list[int]]) -> dict[int, list[int]]:
        if not new_measurements:
            return self._current_state.measurements
        new_measurement = list(new_measurements.values())[0][0]
        local_qubit_index = self._operation.control_encoding.qubit_index
        first_qubit_x = self._operation.control_encoding.encoding.all_qubits[0].x
        global_qubit_index = first_qubit_x + local_qubit_index

        combined_measurements = deepcopy(self._current_state.measurements)
        combined_measurements[global_qubit_index].append(new_measurement)
        return combined_measurements

    def _get_circuit(self) -> Circuit:
        if self._operation.target_encoding:
            return self._get_controlled_circuit() if self._operation.control_encoding else self._target_circuit
        elif self._operation.control_encoding:
            return self._get_measurement_circuit()
        else:
            raise ValueError('Was given a SimulationOperation with no encoding.')

    def _get_controlled_circuit(self) -> Circuit:
        target_controlled_by_ancilla = [operation.controlled_by(self._ancilla_qubit) for operation in self._target_circuit.all_operations()]
        return Circuit(
            self._control_controlled_by_ancilla,
            target_controlled_by_ancilla,
            self._control_controlled_by_ancilla,
        )

    def _get_measurement_circuit(self) -> Circuit:
        return Circuit(
            self._control_controlled_by_ancilla,
            M(self._ancilla_qubit),
            R(self._ancilla_qubit),
        )

    @cached_property
    def _control_controlled_by_ancilla(self) -> Circuit:
        control_controlled_by_ancilla = [operation.controlled_by(self._ancilla_qubit) for operation in self._control_circuit.all_operations()]
        return Circuit(
            H(self._ancilla_qubit),
            control_controlled_by_ancilla,
            H(self._ancilla_qubit),
        )

    @cached_property
    def _control_circuit(self) -> Circuit:
        control_operation = LogicalOperation(
            gate=LogicalGateLabel.Z,
            qubit_index=self._operation.control_encoding.qubit_index
        )
        return self._operation.control_encoding.encoding.get_operation_circuit(operation=control_operation)

    @cached_property
    def _target_circuit(self) -> Circuit:
        return self._operation.target_encoding.encoding.get_operation_circuit(operation=self._operation.target_encoding.operation)

    @property
    def _error_correcting_code_utilities(self) -> ErrorCorrectingCodeUtilities:
        return get_error_correcting_code_utilities(state=self._current_state.state)
