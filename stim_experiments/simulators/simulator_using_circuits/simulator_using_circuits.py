from dataclasses import dataclass
from math import ceil
from typing import List

from proto.utils import cached_property

from stim_experiments.error_correcting_codes.error_correcting_code.error_correcting_code import ErrorCorrectingCode
from stim_experiments.custom_dataclasses.logical_operation import LogicalGateLabel, LogicalOperation
from stim_experiments.error_correcting_codes.generic_stabilizer_code.support.stabilizer_transformer import \
    TransformationGate, TransformationOperation
from stim_experiments.simulators.custom_dataclasses.simulator_result import SimulatorResult


@dataclass
class SimulationOperation:
    operation: LogicalOperation
    encoding: ErrorCorrectingCode


class SimulatorUsingCircuits:
    def __init__(self, error_correcting_code: ErrorCorrectingCode, operations: List[TransformationOperation]):
        self._error_correcting_code = error_correcting_code
        self._operations = operations
        self._transformation_gate_to_logical_gate = {
            TransformationGate.X: LogicalGateLabel.X,
        }

    def simulate(self) -> SimulatorResult:
        for operation in self._operations:
            simulation_operations = self._transformation_operation_to_simulation_operations(transformation_operation=operation)
            for simulation_operation in simulation_operations:
                simulation_operation.encoding.apply_operation(operation=simulation_operation.operation)
        return SimulatorResult(
            encodings=self._encodings,
            measurements={},
        )

    def _transformation_operation_to_simulation_operations(self, transformation_operation: TransformationOperation) -> List[SimulationOperation]:
        target_index_on_encoding = transformation_operation.target_qubit_index % self._error_correcting_code.num_logical_qubits
        encoding_number = transformation_operation.target_qubit_index // self._error_correcting_code.num_logical_qubits
        encoding = self._encodings[encoding_number]
        if transformation_operation.gate == TransformationGate.X:
            return [SimulationOperation(
                operation=LogicalOperation(
                    gate=LogicalGateLabel.X,
                    qubit_index=target_index_on_encoding,
                ),
                encoding=encoding
            )]
        elif transformation_operation.gate == TransformationGate.Z:
            return [SimulationOperation(
                operation=LogicalOperation(
                    gate=LogicalGateLabel.Z,
                    qubit_index=target_index_on_encoding,
                ),
                encoding=encoding
            )]
        raise ValueError(f"Unimplemented transformation gate {transformation_operation.gate}.") # TODO test this

    @cached_property
    def _encodings(self) -> List[ErrorCorrectingCode]:
        num_encodings = ceil(self._num_logical_qubits / self._error_correcting_code.num_logical_qubits)
        return [self._error_correcting_code.create_new() for _ in range(num_encodings)]

    @property
    def _num_logical_qubits(self) -> int:
        largest_index = max(qubit_index for operation in self._operations
                            for qubit_index in (operation.control_qubit_index, operation.target_qubit_index)
                            if qubit_index is not None)
        return largest_index + 1
