from cirq import Circuit, LineQubit, Simulator, StateVectorTrialResult
from numpy import array
from proto.utils import cached_property

from stim_experiments.error_correcting_codes.error_correcting_code_utilities import get_error_correcting_code_utilities
from stim_experiments.error_correcting_codes.generic_stabilizer_code.custom_dataclasses.state_and_measurements import \
    StateAndMeasurements
from stim_experiments.error_correcting_codes.generic_stabilizer_code.custom_dataclasses.transformation_operation import \
    TransformationOperation
from stim_experiments.simulators.simulator_using_circuits.custom_dataclasses.logical_encodings_with_shared_ancillas import \
    LogicalEncodingsWithSharedAncillas
from stim_experiments.simulators.simulator_using_circuits.support.simulation_operations_simulator.simulation_operation_simulator import \
    SimulationOperationSimulator
from stim_experiments.simulators.simulator_using_circuits.support.simulation_operations_simulator.support.circuit_from_operation_creator import \
    CircuitFromOperationCreator
from stim_experiments.simulators.simulator_using_circuits.support.transformation_operation_to_simulation_operation import \
    TransformationOperationToSimulationOperationConverter
from stim_experiments.utilities import TYPE_STATE_VECTOR_OR_DENSITY_MATRIX, is_state_vector, tensor, \
    trace_out_ancillas_in_zero_state


class LogicalOperationsSimulator:
    def __init__(self, encodings: LogicalEncodingsWithSharedAncillas, operations: list[TransformationOperation]):
        self._encodings = encodings
        self._operations = operations

    def simulate(self) -> StateAndMeasurements:
        self._ensure_enough_logical_qubits()

        simulation_operations = [
            TransformationOperationToSimulationOperationConverter(
                transformation_operation=operation,
                encodings=self._encodings.encodings
            ).get_simulation_operation()
            for operation in self._operations
        ]
        circuit_pieces = [
            CircuitFromOperationCreator(operation=simulation_operation,
                                        ancilla_qubits=self._encodings.ancillas,
                                        num_state_qubits=len(self._state_qubits),
                                        ).create_circuit()
            for simulation_operation in simulation_operations
        ]
        circuit = Circuit(circuit_pieces)

        error_correcting_code_utilities = get_error_correcting_code_utilities(state=self._get_initial_state())
        return error_correcting_code_utilities.get_state_after_circuit(circuit=circuit,
                                                                       qubit_order=self._state_qubits,
                                                                       initial_state=self._get_initial_state())

    def _ensure_enough_logical_qubits(self) -> None:
        num_logical_qubits_given = sum(code.num_logical_qubits for code in self._encodings.encodings)
        if num_logical_qubits_given < self._num_logical_qubits_needed:
            raise ValueError(
                f"Not enough logical qubits available. Operations need at least {self._num_logical_qubits_needed} logical qubits,"
                f" but {num_logical_qubits_given} was/were provided.")

    @cached_property
    def _num_logical_qubits_needed(self) -> int:
        qubit_indices_in_operations = [qubit_index for operation in self._operations
                                       for qubit_index in (operation.control_qubit_index, operation.target_qubit_index)
                                       if qubit_index is not None]
        largest_index = max(qubit_indices_in_operations) if qubit_indices_in_operations else -1
        return largest_index + 1

    def _get_initial_state(self) -> TYPE_STATE_VECTOR_OR_DENSITY_MATRIX:
        if not self._encodings.encodings:
            return array([])
        qubit_states_data = [trace_out_ancillas_in_zero_state(state=encoding.encode_logical_qubit(),
                                                              num_ancillas=len(encoding.ancilla_qubits))
                             for encoding in self._encodings.encodings]
        qubit_states_ancilla = [self._encodings.encodings[0].error_correcting_code_utilities.zero_state] * len(self._encodings.ancillas)
        return tensor(*qubit_states_data, *qubit_states_ancilla)

    @cached_property
    def _control_ancilla(self) -> LineQubit:
        return self._encodings.ancillas[0] \
            if self._encodings.ancillas \
            else LineQubit(len(self._state_qubits))

    @cached_property
    def _state_qubits(self) -> list[LineQubit]:
        return [qubit for encoding in self._encodings.encodings for qubit in encoding.data_qubits] + self._encodings.ancillas
