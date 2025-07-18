from cirq import Circuit, LineQubit
from proto.utils import cached_property

from algorithms.support.logical_operations_circuit_creator.support.circuit_from_operation_creator import \
    CircuitFromOperationCreator
from algorithms.support.logical_operations_circuit_creator.support.transformation_operation_to_simulation_operation import \
    TransformationOperationToSimulationOperationConverter
from stim_experiments.custom_dataclasses.transformation_operation import \
    TransformationOperation
from stim_experiments.error_correcting_codes.error_correcting_code.error_correcting_code import ErrorCorrectingCode
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
        encoding_circuits = [
            encoding.encode_logical_qubit()
            for encoding in self._encodings
        ]
        return Circuit(
            encoding_circuits,
            operations_circuits,
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
