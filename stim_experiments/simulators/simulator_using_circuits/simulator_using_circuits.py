from math import ceil
from typing import List

from proto.utils import cached_property

from stim_experiments.error_correcting_codes.error_correcting_code.error_correcting_code import ErrorCorrectingCode
from stim_experiments.custom_dataclasses.logical_operation import LogicalGateLabel, LogicalOperation
from stim_experiments.error_correcting_codes.generic_stabilizer_code.support.stabilizer_transformer import \
    TransformationGate, TransformationOperation
from stim_experiments.simulators.custom_dataclasses.simulator_result import SimulatorResult


class SimulatorUsingCircuits:
    def __init__(self, error_correcting_code: ErrorCorrectingCode, operations: List[TransformationOperation]):
        self._error_correcting_code = error_correcting_code
        self._operations = operations
        self._transformation_gate_to_logical_gate = {
            TransformationGate.X: LogicalGateLabel.X,
        }

    def simulate(self) -> SimulatorResult:
        for operation in self._operations:
            encoding = self._logical_qubits[0]
            logical_operation = LogicalOperation(
                gate=self._transformation_gate_to_logical_gate[operation.gate],
                qubit_index=operation.target_qubit_index,
            )
            encoding.apply_operation(operation=logical_operation)
        return SimulatorResult(
            encodings=self._logical_qubits,
            measurements={},
        )

    @cached_property
    def _logical_qubits(self) -> List[ErrorCorrectingCode]:
        num_encodings = 1
        # num_encodings = ceil(self._num_logical_qubits / self._error_correcting_code.num_logical_qubits)  # tests codes with multiple logical qubit encodings
        return [self._error_correcting_code.create_new() for _ in range(num_encodings)]

    @property
    def _num_logical_qubits(self) -> int:
        unique_indices = {qubit_index for operation in self._operations
                          for qubit_index in (operation.control_qubit_index, operation.target_qubit_index)
                          if qubit_index is not None}
        return len(unique_indices)
