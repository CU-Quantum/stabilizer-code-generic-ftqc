from cirq import Circuit, LineQubit
from proto.utils import cached_property

from stim_experiments.algorithms.support.logical_operations_circuit_creator.support.circuit_from_operation_creator import \
    CircuitFromOperationCreator
from stim_experiments.algorithms.support.logical_operations_circuit_creator.support.transformation_operation_to_simulation_operation import \
    TransformationOperationToSimulationOperationConverter
from stim_experiments.custom_dataclasses.transformation_operation import \
    TransformationOperation
from stim_experiments.error_correcting_codes.error_correcting_code.error_correcting_code import ErrorCorrectingCode
from stim_experiments.globals.active_encodings_store import ActiveEncodingsStore
from stim_experiments.globals.fresh_ancillas_pool import FreshAncillasPool


class LogicalOperationsCircuitCreator:
    def __init__(self, encodings: list[ErrorCorrectingCode], operations: list[TransformationOperation]):
        self._encodings = encodings
        self._operations = operations

    def get_simulation_circuit(self) -> Circuit:
        self._ensure_enough_logical_qubits()
        FreshAncillasPool().set_first_ancilla_num(len(self.data_qubits))

        simulation_operations = [
            TransformationOperationToSimulationOperationConverter(
                transformation_operation=operation,
                encodings=self._encodings
            ).get_simulation_operation()
            for operation in self._operations
        ]
        operations_circuits = [
            CircuitFromOperationCreator(operation=simulation_operation).create_circuit()
            for simulation_operation in simulation_operations
        ]
        encoding_circuit = self._get_snowballed_encodings_with_error_correction(encodings=self._encodings)
        with ActiveEncodingsStore(additional_tracked_encodings=self._encodings) as encodings_store:
            return Circuit(
                encoding_circuit,
                [
                    [
                        operation_circuit,
                        encodings_store.get_all_correction_circuits(),
                    ] for operation_circuit in operations_circuits
                ],
            )

    def _get_snowballed_encodings_with_error_correction(self, encodings: list[ErrorCorrectingCode]) -> Circuit:
        if not encodings:
            return Circuit()
        encoding = encodings[0]
        with ActiveEncodingsStore(additional_tracked_encodings=[encoding]) as encodings_store:
            return Circuit(
                encoding.encode_logical_qubit(),
                encodings_store.get_all_correction_circuits(),
                self._get_snowballed_encodings_with_error_correction(encodings[1:])
            )

    def _ensure_enough_logical_qubits(self) -> None:
        num_logical_qubits_given = sum(code.num_logical_qubits for code in self._encodings)
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

    @cached_property
    def data_qubits(self) -> list[LineQubit]:
        return [qubit for encoding in self._encodings for qubit in encoding.data_qubits]
