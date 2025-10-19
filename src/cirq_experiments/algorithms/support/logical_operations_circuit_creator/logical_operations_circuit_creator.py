from cirq import Circuit, CircuitOperation, FrozenCircuit, LineQubit, TaggedOperation
from proto.utils import cached_property

from cirq_experiments.algorithms.support.logical_operations_circuit_creator.support.circuit_from_operation_creator import \
    CircuitFromOperationCreator, LOGICAL_QUBIT_INDEX_TAG
from cirq_experiments.algorithms.support.logical_operations_circuit_creator.support.transformation_operation_to_simulation_operation import \
    TransformationOperationToSimulationOperationConverter
from cirq_experiments.custom_dataclasses.transformation_operation import \
    TransformationOperation
from cirq_experiments.error_correcting_codes.stabilizer_code.stabilizer_code import StabilizerCode
from cirq_experiments.globals.active_encodings_store import ActiveEncodingsStore
from cirq_experiments.globals.fresh_ancillas_pool import FreshAncillasPool


LOGICAL_QUBIT_ENCODING_TAG = 'LOGICAL_QUBIT_ENCODING'


class LogicalOperationsCircuitCreator:
    def __init__(self, encodings: list[StabilizerCode], operations: list[TransformationOperation]):
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
        encoding_circuits = self._get_snowballed_encodings_with_error_correction(encodings=self._encodings)
        with ActiveEncodingsStore(additional_tracked_encodings=self._encodings) as encodings_store:
            operations_circuits = [
                CircuitFromOperationCreator(operation=simulation_operation, operation_index=i).create_circuit()
                for i, simulation_operation in enumerate(simulation_operations)
            ]
            return Circuit(
                encoding_circuits,
                [
                    [
                        operation_circuit,
                        encodings_store.get_all_correction_circuits(),
                    ] for operation_circuit in operations_circuits[:-1]
                ],
                operations_circuits[-1] if operations_circuits else []
            )

    def _get_snowballed_encodings_with_error_correction(self, encodings: list[StabilizerCode]) -> Circuit:
        if not encodings:
            return Circuit()
        encoding = encodings[0]
        with ActiveEncodingsStore(additional_tracked_encodings=[encoding]) as encodings_store:
            return Circuit(
                TaggedOperation(
                    CircuitOperation(
                        FrozenCircuit(
                            encoding.encode_logical_qubit(),
                            encodings_store.get_all_correction_circuits(),
                            self._get_snowballed_encodings_with_error_correction(encodings[1:])
                        ),
                    ),
                    LOGICAL_QUBIT_ENCODING_TAG, f'{LOGICAL_QUBIT_INDEX_TAG}_{len(self._encodings) - len(encodings)}'
                )
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
