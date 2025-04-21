from cirq import LineQubit, kron
from numpy import array, ceil
from proto.utils import cached_property

from stim_experiments.error_correcting_codes.error_correcting_code.error_correcting_code import ErrorCorrectingCode
from stim_experiments.error_correcting_codes.generic_stabilizer_code.custom_dataclasses.state_and_measurements import \
    StateAndMeasurements
from stim_experiments.error_correcting_codes.generic_stabilizer_code.custom_dataclasses.transformation_operation import \
    TransformationOperation
from stim_experiments.simulators.simulator_using_circuits.custom_dataclasses.simulation_operation import \
    SimulationOperation
from stim_experiments.simulators.simulator_using_circuits.support.transformation_operation_to_simulation_operation import \
    TransformationOperationToSimulationOperationConverter
from stim_experiments.simulators.simulator_using_circuits.support.simulation_operation_performer import \
    SimulationOperationPerformer
from stim_experiments.utilities import TYPE_STATE_VECTOR_OR_DENSITY_MATRIX, trace_out_ancillas_in_zero_state


class SimulatorUsingCircuits:
    def __init__(self, error_correcting_codes: ErrorCorrectingCode | list[ErrorCorrectingCode], operations: list[TransformationOperation]):
        """

        :param error_correcting_codes: use instance of a code to encode all logical qubits with that code, or use a list of codes to specify the encodings of each logical qubit
        :param operations: operations for the simulator to perform on the logical qubits
        """
        self._error_correcting_codes = error_correcting_codes
        self._operations = operations

        self._all_encodings_provided = isinstance(self._error_correcting_codes, list)

    def simulate(self) -> StateAndMeasurements:
        state = StateAndMeasurements(state=self._initialize_state(),)
        for operation in self._operations:
            simulation_operation = self._transformation_operation_to_simulation_operations(transformation_operation=operation)
            ancilla_qubit = self._shared_ancilla_qubits[0] \
                if self._shared_ancilla_qubits\
                else LineQubit(len(self._all_qubits))
            state = SimulationOperationPerformer(operation=simulation_operation,
                                                 current_state=state,
                                                 qubits=self._all_qubits,
                                                 ancilla_qubit=ancilla_qubit,
                                                 ).perform_operation()
        return state

    def _initialize_state(self) -> TYPE_STATE_VECTOR_OR_DENSITY_MATRIX:
        if not self._encodings:
            return array([])
        qubit_states_data = [trace_out_ancillas_in_zero_state(state=encoding.encode_logical_qubit(),
                                                              num_ancillas=len(encoding.ancilla_qubits))
                             for encoding in self._encodings]
        qubit_states_ancilla = [self._encodings[0].error_correcting_code_utilities.zero_state] * len(self._shared_ancilla_qubits)
        return kron(*qubit_states_data, *qubit_states_ancilla, shape_len=len(qubit_states_data[0].shape))

    def _transformation_operation_to_simulation_operations(self, transformation_operation: TransformationOperation) -> SimulationOperation:
        return TransformationOperationToSimulationOperationConverter(transformation_operation=transformation_operation,
                                                                     encodings=self._encodings).get_simulation_operation()

    @cached_property
    def _all_qubits(self) -> list[LineQubit]:
        return [qubit for encoding in self._encodings for qubit in encoding.data_qubits] + self._shared_ancilla_qubits

    @cached_property
    def _encodings(self) -> list[ErrorCorrectingCode]:
        return self._use_given_codes_for_encodings() \
            if self._all_encodings_provided \
            else self._use_one_code_for_all_encodings()

    def _use_one_code_for_all_encodings(self) -> list[ErrorCorrectingCode]:
        return [
            self._error_correcting_codes.create_new(
                qubit_start_index=i * len(self._error_correcting_codes.data_qubits),
                provided_ancilla_qubits=self._shared_ancilla_qubits
            )
            for i in range(self._num_encodings)
        ]

    def _use_given_codes_for_encodings(self) -> list[ErrorCorrectingCode]:
        num_logical_qubits_given = sum(code.num_logical_qubits for code in self._error_correcting_codes)
        if num_logical_qubits_given < self._num_logical_qubits_needed:
            raise ValueError(
                f"Not enough logical qubits available. Operations need at least {self._num_logical_qubits_needed} logical qubits,"
                f" but {num_logical_qubits_given} was/were provided.")

        encodings = []
        current_index = 0
        for code in self._error_correcting_codes:
            new_code = code.create_new(
                qubit_start_index=current_index,
                provided_ancilla_qubits=self._shared_ancilla_qubits[:len(code.ancilla_qubits)]
            )
            encodings.append(new_code)
            current_index += len(new_code.data_qubits)

        return encodings

    @cached_property
    def _num_logical_qubits_needed(self) -> int:
        qubit_indices_in_operations = [qubit_index for operation in self._operations
                                       for qubit_index in (operation.control_qubit_index, operation.target_qubit_index)
                                       if qubit_index is not None]
        largest_index = max(qubit_indices_in_operations) if qubit_indices_in_operations else -1
        return largest_index + 1

    @cached_property
    def _shared_ancilla_qubits(self) -> list[LineQubit]:
        if self._all_encodings_provided:
            num_shared_ancilla_qubits = max(len(code.ancilla_qubits) for code in self._error_correcting_codes)
            start_index = sum(len(code.data_qubits) for code in self._error_correcting_codes)
        else:
            num_shared_ancilla_qubits = len(self._error_correcting_codes.ancilla_qubits)
            start_index = len(self._error_correcting_codes.data_qubits) * self._num_encodings
        return LineQubit.range(start_index, start_index + num_shared_ancilla_qubits)

    @cached_property
    def _num_encodings(self) -> int:
        if self._all_encodings_provided:
            return len(self._error_correcting_codes)
        qubits_per_code = self._error_correcting_codes.num_logical_qubits
        return int(ceil(self._num_logical_qubits_needed / qubits_per_code))
