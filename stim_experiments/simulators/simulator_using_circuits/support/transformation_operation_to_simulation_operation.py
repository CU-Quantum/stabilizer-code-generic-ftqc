from dataclasses import replace
from functools import cached_property
from typing import List

from stim_experiments.custom_dataclasses.logical_operation import LogicalGateLabel, LogicalOperation
from stim_experiments.error_correcting_codes.error_correcting_code.error_correcting_code import ErrorCorrectingCode
from stim_experiments.error_correcting_codes.generic_stabilizer_code.custom_dataclasses.transformation_operation import \
    TransformationGate, TransformationOperation
from stim_experiments.simulators.simulator_using_circuits.custom_dataclasses.simulation_operation import \
    LogicalEncodingIndex, SimulationOperation, TargetEncoding


class TransformationOperationToSimulationOperationConverter:
    def __init__(self, transformation_operation: TransformationOperation, encodings: List[ErrorCorrectingCode]):
        self._transformation_operation = transformation_operation
        self._encodings = encodings

    def get_simulation_operation(self) -> SimulationOperation:
        self._transformation_operation.validate()
        if self._transformation_operation.gate == TransformationGate.M:
            return SimulationOperation(control_encoding=self._target_encoding)
        operation = self._get_target_operation()
        if self._transformation_operation.control_qubit_index is not None:
            operation = self._add_control(operation)
        return operation

    def _get_target_operation(self) -> SimulationOperation:
        logical_gate_label = self._get_logical_gate_label()
        return SimulationOperation(
            target_encoding=TargetEncoding(
                operation=LogicalOperation(
                    gate=logical_gate_label,
                    qubit_index=self._target_encoding.qubit_index,
                ),
                encoding=self._target_encoding.encoding,
            ),
        )

    @cached_property
    def _target_encoding(self) -> LogicalEncodingIndex:
        return self._get_encoding(qubit_index=self._transformation_operation.target_qubit_index)

    def _add_control(self, operation: SimulationOperation) -> SimulationOperation:
        encoding_control = self._get_encoding(qubit_index=self._transformation_operation.control_qubit_index)
        return replace(operation, control_encoding=encoding_control)

    def _get_logical_gate_label(self) -> LogicalGateLabel:
        if self._transformation_operation.gate == TransformationGate.X:
            return LogicalGateLabel.X
        elif self._transformation_operation.gate == TransformationGate.Z:
            return LogicalGateLabel.Z
        elif self._transformation_operation.gate == TransformationGate.H:
            return LogicalGateLabel.H
        elif self._transformation_operation.gate == TransformationGate.CX:
            return LogicalGateLabel.X
        elif self._transformation_operation.gate == TransformationGate.CZ:
            return LogicalGateLabel.Z
        raise ValueError(f"Unimplemented transformation gate {self._transformation_operation.gate}.") # TODO test this

    def _get_encoding(self, qubit_index: int) -> LogicalEncodingIndex:
        current_index = 0
        found_encoding = self._encodings[-1]
        for encoding in self._encodings:
            if current_index <= qubit_index < current_index + encoding.num_logical_qubits:
                found_encoding = encoding
                break
            current_index += encoding.num_logical_qubits
        return LogicalEncodingIndex(
            encoding=found_encoding,
            qubit_index=qubit_index - current_index,
        )
