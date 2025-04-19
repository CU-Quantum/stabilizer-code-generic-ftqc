from typing import List

from cirq import Circuit, H, LineQubit, kron
from proto.utils import cached_property

from stim_experiments.custom_dataclasses.logical_operation import LogicalGateLabel, LogicalOperation
from stim_experiments.error_correcting_codes.generic_stabilizer_code.error_correcting_code_utilities import \
    ErrorCorrectingCodeUtilities
from stim_experiments.error_correcting_codes.utilities import get_error_correcting_code_utilities, is_state_vector
from stim_experiments.simulators.simulator_using_circuits.custom_dataclasses.simulation_operation import \
    SimulationOperation
from stim_experiments.utilities import TYPE_STATE_VECTOR_OR_DENSITY_MATRIX, partial_trace


class SimulationOperationPerformer:
    def __init__(self, operation: SimulationOperation, current_state: TYPE_STATE_VECTOR_OR_DENSITY_MATRIX, qubits: List[LineQubit]):
        self._operation = operation
        self._current_state = current_state
        self._qubits = qubits

    def get_state(self) -> TYPE_STATE_VECTOR_OR_DENSITY_MATRIX:
        return self._perform_controlled_operation() \
            if self._operation.control_encoding \
            else self._perform_uncontrolled_operation()

    def _perform_controlled_operation(self) -> TYPE_STATE_VECTOR_OR_DENSITY_MATRIX:
        ancilla_state = self._error_correcting_code_utilities.zero_state
        state = kron(self._current_state, ancilla_state, shape_len=len(self._current_state.shape))
        circuit = self._get_controlled_circuit()
        state = self._error_correcting_code_utilities.get_state_after_circuit(circuit=circuit,
                                                                              qubit_order=self._qubits + [self._ancilla_qubit],
                                                                              initial_state=state)
        return self._trace_out_ancilla(state=state)

    def _perform_uncontrolled_operation(self) -> TYPE_STATE_VECTOR_OR_DENSITY_MATRIX:
        return self._error_correcting_code_utilities.get_state_after_circuit(circuit=self._target_circuit,
                                                                             qubit_order=self._qubits,
                                                                             initial_state=self._current_state)

    def _get_controlled_circuit(self):
        control_controlled_by_ancilla = [operation.controlled_by(self._ancilla_qubit) for operation in self._control_circuit.all_operations()]
        target_controlled_by_ancilla = [operation.controlled_by(self._ancilla_qubit) for operation in self._target_circuit.all_operations()]
        circuit = Circuit(
            H(self._ancilla_qubit),
            control_controlled_by_ancilla,
            H(self._ancilla_qubit),
            target_controlled_by_ancilla,
            H(self._ancilla_qubit),
            control_controlled_by_ancilla,
            H(self._ancilla_qubit)
        )
        return circuit

    def _trace_out_ancilla(self, state: TYPE_STATE_VECTOR_OR_DENSITY_MATRIX) -> TYPE_STATE_VECTOR_OR_DENSITY_MATRIX:
        if is_state_vector(state=state):
            return state[[not i % 2 for i in range(len(state))]]  # ancilla will be in |0>, so can take every other value
        else:
            return partial_trace(rho=state, keep_qubits=list(range(len(self._qubits))))

    @cached_property
    def _control_circuit(self) -> Circuit:
        control_operation = LogicalOperation(
            gate=LogicalGateLabel.Z,
            qubit_index=self._operation.control_encoding.qubit_index
        )
        return self._operation.control_encoding.encoding.get_operation_circuit(operation=control_operation)

    @cached_property
    def _target_circuit(self) -> Circuit:
        return self._operation.encoding.get_operation_circuit(operation=self._operation.operation)

    @cached_property
    def _ancilla_qubit(self) -> LineQubit:
        return LineQubit(self._num_qubits)

    @property
    def _num_qubits(self) -> int:
        return len(self._qubits)

    @property
    def _error_correcting_code_utilities(self) -> ErrorCorrectingCodeUtilities:
        return get_error_correcting_code_utilities(state=self._current_state)
