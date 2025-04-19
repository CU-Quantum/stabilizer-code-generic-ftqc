from dataclasses import replace
from typing import List

from stim_experiments.custom_dataclasses.logical_operation import LogicalGateLabel, LogicalOperation
from stim_experiments.error_correcting_codes.error_correcting_code.error_correcting_code import ErrorCorrectingCode
from stim_experiments.error_correcting_codes.generic_stabilizer_code.support.stabilizer_transformer import \
    TransformationGate, TransformationOperation
from stim_experiments.simulators.simulator_using_circuits.custom_dataclasses.simulation_operation import \
    ControlEncoding, SimulationOperation


class TransformationOperationToSimulationOperationConverter:
    def __init__(self, transformation_operation: TransformationOperation, encodings: List[ErrorCorrectingCode]):
        self._transformation_operation = transformation_operation
        self._encodings = encodings

    def get_simulation_operation(self) -> SimulationOperation:
        operation = self._get_target_operation()
        if self._transformation_operation.control_qubit_index is not None:
            operation = self._add_control(operation)
        return operation

    def _get_target_operation(self) -> SimulationOperation:
        logical_gate_label = self._get_logical_gate_label()
        target_encoding = self._get_encoding(qubit_index=self._transformation_operation.target_qubit_index)
        target_index_on_encoding = self._get_index_on_encoding(
            qubit_index=self._transformation_operation.target_qubit_index)
        return SimulationOperation(
            operation=LogicalOperation(
                gate=logical_gate_label,
                qubit_index=target_index_on_encoding,
            ),
            encoding=target_encoding
        )

    def _add_control(self, operation: SimulationOperation) -> SimulationOperation:
        encoding_control = self._get_encoding(qubit_index=self._transformation_operation.control_qubit_index)
        control_index_on_encoding = self._get_index_on_encoding(
            qubit_index=self._transformation_operation.control_qubit_index)
        return replace(operation, control_encoding=ControlEncoding(
            encoding=encoding_control,
            qubit_index=control_index_on_encoding,
        ))

    def _get_logical_gate_label(self) -> LogicalGateLabel:
        if self._transformation_operation.gate == TransformationGate.X:
            return LogicalGateLabel.X
        elif self._transformation_operation.gate == TransformationGate.Z:
            return LogicalGateLabel.Z
        elif self._transformation_operation.gate == TransformationGate.H:
            return LogicalGateLabel.H
        elif self._transformation_operation.gate == TransformationGate.CX:
            return LogicalGateLabel.X
        raise ValueError(f"Unimplemented transformation gate {self._transformation_operation.gate}.") # TODO test this

    def _get_encoding(self, qubit_index: int) -> ErrorCorrectingCode:
        encoding_number_control = qubit_index // self._num_logical_qubits
        return self._encodings[encoding_number_control]

    def _get_index_on_encoding(self, qubit_index: int) -> int:
        return qubit_index % self._num_logical_qubits

    @property
    def _num_logical_qubits(self) -> int:
        return self._encodings[0].num_logical_qubits
