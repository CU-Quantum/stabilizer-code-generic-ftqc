from cirq import LineQubit, kron
from numpy import array
from proto.utils import cached_property

from stim_experiments.error_correcting_codes.generic_stabilizer_code.custom_dataclasses.state_and_measurements import \
    StateAndMeasurements
from stim_experiments.error_correcting_codes.generic_stabilizer_code.custom_dataclasses.transformation_operation import \
    TransformationOperation
from stim_experiments.simulators.simulator_using_circuits.custom_dataclasses.logical_encodings_with_shared_ancillas import \
    LogicalEncodingsWithSharedAncillas
from stim_experiments.simulators.simulator_using_circuits.custom_dataclasses.simulation_operation import \
    SimulationOperation
from stim_experiments.simulators.simulator_using_circuits.support.transformation_operation_to_simulation_operation import \
    TransformationOperationToSimulationOperationConverter
from stim_experiments.simulators.simulator_using_circuits.support.simulation_operation_performer import \
    SimulationOperationPerformer
from stim_experiments.utilities import TYPE_STATE_VECTOR_OR_DENSITY_MATRIX, trace_out_ancillas_in_zero_state


class SimulatorUsingCircuits:
    def __init__(self, encodings: LogicalEncodingsWithSharedAncillas, operations: list[TransformationOperation]):
        """

        :param error_correcting_codes: use instance of a code to encode all logical qubits with that code, or use a list of codes to specify the encodings of each logical qubit
        :param operations: operations for the simulator to perform on the logical qubits
        """
        self._encodings = encodings
        self._operations = operations

    def simulate(self) -> StateAndMeasurements:
        self._ensure_enough_logical_qubits()

        state = StateAndMeasurements(state=self._initialize_state(),)
        for operation in self._operations:
            simulation_operation = self._transformation_operation_to_simulation_operations(transformation_operation=operation)
            ancilla_qubit = self._encodings.ancillas[0] \
                if self._encodings.ancillas \
                else LineQubit(len(self._all_qubits))
            state = SimulationOperationPerformer(operation=simulation_operation,
                                                 current_state=state,
                                                 qubits=self._all_qubits,
                                                 ancilla_qubit=ancilla_qubit,
                                                 ).perform_operation()
        return state

    def _ensure_enough_logical_qubits(self) -> None:
        num_logical_qubits_given = sum(code.num_logical_qubits for code in self._encodings.encodings)
        if num_logical_qubits_given < self._num_logical_qubits_needed:
            raise ValueError(
                f"Not enough logical qubits available. Operations need at least {self._num_logical_qubits_needed} logical qubits,"
                f" but {num_logical_qubits_given} was/were provided.")

    def _initialize_state(self) -> TYPE_STATE_VECTOR_OR_DENSITY_MATRIX:
        if not self._encodings:
            return array([])
        qubit_states_data = [trace_out_ancillas_in_zero_state(state=encoding.encode_logical_qubit(),
                                                              num_ancillas=len(encoding.ancilla_qubits))
                             for encoding in self._encodings.encodings]
        qubit_states_ancilla = [self._encodings.encodings[0].error_correcting_code_utilities.zero_state] * len(self._encodings.ancillas)
        return kron(*qubit_states_data, *qubit_states_ancilla, shape_len=len(qubit_states_data[0].shape))

    def _transformation_operation_to_simulation_operations(self, transformation_operation: TransformationOperation) -> SimulationOperation:
        return TransformationOperationToSimulationOperationConverter(transformation_operation=transformation_operation,
                                                                     encodings=self._encodings.encodings).get_simulation_operation()

    @cached_property
    def _all_qubits(self) -> list[LineQubit]:
        return [qubit for encoding in self._encodings.encodings for qubit in encoding.data_qubits] + self._encodings.ancillas

    @cached_property
    def _num_logical_qubits_needed(self) -> int:
        qubit_indices_in_operations = [qubit_index for operation in self._operations
                                       for qubit_index in (operation.control_qubit_index, operation.target_qubit_index)
                                       if qubit_index is not None]
        largest_index = max(qubit_indices_in_operations) if qubit_indices_in_operations else -1
        return largest_index + 1
