from typing import List

from cirq import Circuit, H, LineQubit, M, kron
from proto.utils import cached_property

from stim_experiments.custom_dataclasses.logical_operation import LogicalGateLabel, LogicalOperation
from stim_experiments.error_correcting_codes.generic_stabilizer_code.error_correcting_code_utilities import \
    ErrorCorrectingCodeUtilities
from stim_experiments.error_correcting_codes.generic_stabilizer_code.custom_dataclasses.state_and_measurements import \
    StateAndMeasurements
from stim_experiments.error_correcting_codes.utilities import get_error_correcting_code_utilities, is_state_vector
from stim_experiments.simulators.simulator_using_circuits.custom_dataclasses.simulation_operation import \
    SimulationOperation
from stim_experiments.utilities import TYPE_STATE_VECTOR_OR_DENSITY_MATRIX, partial_trace


class SimulationOperationPerformer:
    def __init__(self, operation: SimulationOperation, current_state: StateAndMeasurements, qubits: List[LineQubit]):
        self._operation = operation
        self._current_state = current_state
        self._qubits = qubits

    def perform_operation(self) -> StateAndMeasurements:
        ancilla_state = self._error_correcting_code_utilities.zero_state
        state = kron(self._current_state.state, ancilla_state, shape_len=len(self._current_state.state.shape))

        if self._operation.target_encoding:
            if self._operation.control_encoding:
                target_controlled_by_ancilla = [operation.controlled_by(self._ancilla_qubit) for operation in self._target_circuit.all_operations()]
                circuit = Circuit(
                    self._control_controlled_by_ancilla,
                    target_controlled_by_ancilla,
                    self._control_controlled_by_ancilla,
                )
            else:
                circuit = self._target_circuit
        elif self._operation.control_encoding:
            circuit = Circuit(
                self._control_controlled_by_ancilla,
                M(self._ancilla_qubit)
            )
        else:
            raise ValueError('Was given a SimulationOperation with no encoding.')

        result = self._error_correcting_code_utilities.get_state_after_circuit(circuit=circuit,
                                                                               qubit_order=self._qubits + [self._ancilla_qubit],
                                                                               initial_state=state)
        return StateAndMeasurements(
            state=self._trace_out_ancilla(result=result),
            measurements=result.measurements,
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

    def _trace_out_ancilla(self, result: StateAndMeasurements) -> TYPE_STATE_VECTOR_OR_DENSITY_MATRIX:
        if is_state_vector(state=result.state):
            measured_one = bool(result.measurements and result.measurements[0])
            return result.state[[not (i + measured_one) % 2 for i in range(len(result.state))]]  # take every other value depending on ancilla in |0> or |1>
        else:
            return partial_trace(rho=result.state, keep_qubits=list(range(len(self._qubits))))

    @cached_property
    def _ancilla_qubit(self) -> LineQubit:
        return LineQubit(self._num_qubits)

    @property
    def _num_qubits(self) -> int:
        return len(self._qubits)

    @property
    def _error_correcting_code_utilities(self) -> ErrorCorrectingCodeUtilities:
        return get_error_correcting_code_utilities(state=self._current_state.state)
