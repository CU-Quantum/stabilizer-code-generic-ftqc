from copy import deepcopy
from typing import List

from cirq import Circuit, LineQubit
from numpy import array

from stim_experiments.error_correcting_codes.generic_stabilizer_code.error_correcting_code_utilities import \
    ErrorCorrectingCodeUtilities
from stim_experiments.error_correcting_codes.generic_stabilizer_code.custom_dataclasses.state_and_measurements import \
    StateAndMeasurements
from stim_experiments.error_correcting_codes.utilities import get_error_correcting_code_utilities
from stim_experiments.utilities import TYPE_STATE_VECTOR_OR_DENSITY_MATRIX, tensor, trace_out_ancillas_in_zero_state


class CircuitSimulator:
    def __init__(self,
                 circuit: Circuit,
                 qubits: List[LineQubit],
                 ancilla_qubit: LineQubit):
        self._circuit = circuit
        self._qubits = qubits
        self._ancilla_qubit = ancilla_qubit

    def simulate(self) -> StateAndMeasurements:
        result = self._run_simulation(circuit=self._circuit)
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
            state = tensor(self._qubits_state, ancilla_state)
            simulated_state_and_measurements = self._error_correcting_code_utilities.get_state_after_circuit(
                circuit=circuit,
                qubit_order=self._qubits + [self._ancilla_qubit],
                initial_state=state)
            return StateAndMeasurements(
                state=trace_out_ancillas_in_zero_state(simulated_state_and_measurements.state, num_ancillas=1),
                measurements=simulated_state_and_measurements.measurements,
            )

    @property
    def _qubits_state(self) -> TYPE_STATE_VECTOR_OR_DENSITY_MATRIX:
        if not self._encodings.encodings:
            return array([])
        qubit_states_data = [trace_out_ancillas_in_zero_state(state=encoding.encode_logical_qubit(),
                                                              num_ancillas=len(encoding.ancilla_qubits))
                             for encoding in self._encodings.encodings]
        qubit_states_ancilla = [self._encodings.encodings[0].error_correcting_code_utilities.zero_state] * len(
            self._encodings.ancillas)
        return tensor(*qubit_states_data, *qubit_states_ancilla)

    def _combine_measurements(self, new_measurements: dict[int, list[int]]) -> dict[int, list[int]]:
        if not new_measurements:
            return self._current_state.measurements

        combined_measurements = deepcopy(self._current_state.measurements)
        for qubit_index, measurement in new_measurements.items():
            combined_measurements[qubit_index].extend(measurement)
        return combined_measurements

    @property
    def _error_correcting_code_utilities(self) -> ErrorCorrectingCodeUtilities:
        return get_error_correcting_code_utilities(state=self._current_state.state)
