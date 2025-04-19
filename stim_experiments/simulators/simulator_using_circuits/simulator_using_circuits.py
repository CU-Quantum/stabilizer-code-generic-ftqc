from dataclasses import dataclass
from math import ceil
from typing import List, Optional

from cirq import Circuit, H, LineQubit, kron
from cirq.ops import qubit_order
from numpy import array
from proto.utils import cached_property

from stim_experiments.error_correcting_codes.error_correcting_code.error_correcting_code import ErrorCorrectingCode
from stim_experiments.custom_dataclasses.logical_operation import LogicalGateLabel, LogicalOperation
from stim_experiments.error_correcting_codes.generic_stabilizer_code.error_correcting_code_utilities import \
    ErrorCorrectingCodeUtilities
from stim_experiments.error_correcting_codes.generic_stabilizer_code.support.stabilizer_transformer import \
    TransformationGate, TransformationOperation
from stim_experiments.error_correcting_codes.utilities import get_error_correcting_code_utilities
from stim_experiments.simulators.custom_dataclasses.simulator_result import SimulatorResult
from stim_experiments.utilities import TYPE_STATE_VECTOR_OR_DENSITY_MATRIX, partial_trace


@dataclass
class SimulationOperation:
    operation: LogicalOperation
    encoding: ErrorCorrectingCode


class SimulatorUsingCircuits:
    def __init__(self, error_correcting_code: ErrorCorrectingCode, operations: List[TransformationOperation]):
        self._error_correcting_code = error_correcting_code
        self._operations = operations
        self._current_state = array([])

    def simulate(self) -> SimulatorResult:
        self._current_state = self._initialize_state()
        for operation in self._operations:
            simulation_operations = self._transformation_operation_to_simulation_operations(transformation_operation=operation)
            if len(simulation_operations) > 1:
                ancilla = LineQubit(len(self._all_qubits))
                state = kron(self._current_state, self._error_correcting_code_utilities.zero_state,
                             shape_len=len(self._current_state.shape))

                control_operation = simulation_operations[0]
                target_operation = simulation_operations[1]
                control_circuit = control_operation.encoding.get_operation_circuit(operation=control_operation.operation)
                target_circuit = target_operation.encoding.get_operation_circuit(operation=target_operation.operation)
                control_controlled_by_ancilla = [operation.controlled_by(ancilla) for operation in control_circuit.all_operations()]
                target_controlled_by_ancilla = [operation.controlled_by(ancilla) for operation in target_circuit.all_operations()]

                circuit = Circuit(
                    H(ancilla),
                    control_controlled_by_ancilla,
                    H(ancilla),
                    target_controlled_by_ancilla,
                    H(ancilla),
                    control_controlled_by_ancilla,
                    H(ancilla)
                )
                state = self._error_correcting_code_utilities.get_state_after_circuit(circuit=circuit,
                                                                                      qubit_order=self._all_qubits + [ancilla],
                                                                                      initial_state=state)
                self._current_state = state[[not i % 2 for i in range(len(state))]]
            else:
                circuit = simulation_operations[0].encoding.get_operation_circuit(operation=simulation_operations[0].operation)
                self._current_state = self._error_correcting_code_utilities.get_state_after_circuit(circuit=circuit,
                                                                                                    qubit_order=self._all_qubits,
                                                                                                    initial_state=self._current_state)

        return SimulatorResult(
            current_state=self._current_state,
            measurements={},
        )

    def _initialize_state(self) -> TYPE_STATE_VECTOR_OR_DENSITY_MATRIX:
        qubit_states = [encoding.encode_logical_qubit() for encoding in self._encodings]
        return kron(*qubit_states, shape_len=len(qubit_states[0].shape)) if qubit_states else array([])

    def _transformation_operation_to_simulation_operations(self, transformation_operation: TransformationOperation) -> List[SimulationOperation]:
        target_index_on_encoding = transformation_operation.target_qubit_index % self._error_correcting_code.num_logical_qubits
        encoding_number_target = transformation_operation.target_qubit_index // self._error_correcting_code.num_logical_qubits
        encoding_target = self._encodings[encoding_number_target]

        if transformation_operation.control_qubit_index is not None:
            control_index_on_encoding = transformation_operation.control_qubit_index % self._error_correcting_code.num_logical_qubits
            encoding_number_control = transformation_operation.control_qubit_index // self._error_correcting_code.num_logical_qubits
            encoding_control = self._encodings[encoding_number_control]

        if transformation_operation.gate == TransformationGate.X:
            return [SimulationOperation(
                operation=LogicalOperation(
                    gate=LogicalGateLabel.X,
                    qubit_index=target_index_on_encoding,
                ),
                encoding=encoding_target
            )]
        elif transformation_operation.gate == TransformationGate.Z:
            return [SimulationOperation(
                operation=LogicalOperation(
                    gate=LogicalGateLabel.Z,
                    qubit_index=target_index_on_encoding,
                ),
                encoding=encoding_target
            )]
        elif transformation_operation.gate == TransformationGate.H:
            return [SimulationOperation(
                operation=LogicalOperation(
                    gate=LogicalGateLabel.H,
                    qubit_index=target_index_on_encoding,
                ),
                encoding=encoding_target
            )]
        elif transformation_operation.gate == TransformationGate.CX:
            return [
                SimulationOperation(
                    operation=LogicalOperation(
                        gate=LogicalGateLabel.Z,
                        qubit_index=control_index_on_encoding,
                    ),
                    encoding=encoding_control
                ),
                SimulationOperation(
                    operation=LogicalOperation(
                        gate=LogicalGateLabel.X,
                        qubit_index=target_index_on_encoding,
                    ),
                    encoding=encoding_target
                ),
            ]
        raise ValueError(f"Unimplemented transformation gate {transformation_operation.gate}.") # TODO test this

    @property
    def _error_correcting_code_utilities(self) -> ErrorCorrectingCodeUtilities:
        return get_error_correcting_code_utilities(state=self._current_state)

    @cached_property
    def _all_qubits(self) -> List[LineQubit]:
        return [qubit for encoding in self._encodings for qubit in encoding.all_qubits]

    @cached_property
    def _encodings(self) -> List[ErrorCorrectingCode]:
        num_encodings = ceil(self._num_logical_qubits / self._error_correcting_code.num_logical_qubits)
        return [self._error_correcting_code.create_new(qubit_start_index=i * len(self._error_correcting_code.all_qubits))
                for i in range(num_encodings)]

    @property
    def _num_logical_qubits(self) -> int:
        qubit_indices_in_operations = [qubit_index for operation in self._operations
                                       for qubit_index in (operation.control_qubit_index, operation.target_qubit_index)
                                       if qubit_index is not None]
        largest_index = max(qubit_indices_in_operations) if qubit_indices_in_operations else -1
        return largest_index + 1
