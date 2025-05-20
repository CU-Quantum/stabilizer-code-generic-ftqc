from typing import Optional

from cirq import Circuit, X, Z

from stim_experiments.custom_dataclasses.logical_operation import LogicalGateLabel, LogicalOperation
from stim_experiments.error_correcting_codes.error_correcting_code.error_correcting_code import ErrorCorrectingCode



class DoubleQubitDoubleLogicalCode(ErrorCorrectingCode):
    def __init__(self, qubits: Optional[list[int]] = None):
        super().__init__(num_data_qubits=2, num_logical_qubits=2, qubits=qubits)

    def encode_logical_qubit(self) -> Circuit:
        return Circuit()

    def get_error_correction_circuit(self) -> Circuit:
        return Circuit()

    def _perform_get_operation_circuit(self, operation: LogicalOperation) -> Optional[Circuit]:
        if operation.gate == LogicalGateLabel.X:
            return Circuit(
                X(self.data_qubits[operation.qubit_index]),
            )
        if operation.gate == LogicalGateLabel.Z:
            return Circuit(
                Z(self.data_qubits[operation.qubit_index]),
            )
        return None
