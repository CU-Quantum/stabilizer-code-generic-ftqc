from cirq import Circuit, I, LineQubit
from proto.utils import cached_property

from stim_experiments.custom_dataclasses.transformation_operation import \
    TransformationOperation
from stim_experiments.globals.fresh_ancillas_pool import FreshAncillasPool
from stim_experiments.simulators.simulator_using_circuits.custom_dataclasses.logical_encodings_with_shared_ancillas import \
    LogicalEncodingsWithSharedAncillas
from stim_experiments.simulators.simulator_using_circuits.support.simulation_operations_simulator.support.circuit_from_operation_creator import \
    CircuitFromOperationCreator
from stim_experiments.simulators.simulator_using_circuits.support.transformation_operation_to_simulation_operation import \
    TransformationOperationToSimulationOperationConverter


class LogicalOperationsCircuitCreator:
    def __init__(self, encodings: LogicalEncodingsWithSharedAncillas, operations: list[TransformationOperation]):
        self._encodings = encodings
        self._operations = operations

    def get_simulation_circuit(self) -> Circuit:
        self._ensure_enough_logical_qubits()
        FreshAncillasPool().set_first_ancilla_num(len(self._state_qubits))

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
        return Circuit(
            [I(qubit) for qubit in self._state_qubits],
            circuit_pieces
        )

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

    @cached_property
    def _state_qubits(self) -> list[LineQubit]:
        return [qubit for encoding in self._encodings.encodings for qubit in encoding.data_qubits]
