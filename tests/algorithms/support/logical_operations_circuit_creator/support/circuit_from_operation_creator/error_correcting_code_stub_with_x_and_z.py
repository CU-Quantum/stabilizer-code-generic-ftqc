from typing import Optional

from cirq import Circuit, LineQubit, X, Z

from stim_experiments.custom_dataclasses.correction_circuit import CorrectionCircuit
from stim_experiments.custom_dataclasses.logical_operation import LogicalGateLabel, LogicalOperation
from stim_experiments.error_correcting_codes.error_correcting_code.error_correcting_code import ErrorCorrectingCode


class ErrorCorrectingCodeStubWithXAndZ(ErrorCorrectingCode):
    def __init__(self, qubits: Optional[list[LineQubit]] = None):
        super().__init__(num_data_qubits=1,
                         num_logical_qubits=1,
                         qubits=qubits)

    def encode_logical_qubit(self):
        pass

    def get_error_correction_circuit(self) -> CorrectionCircuit:
        pass

    def _perform_get_operation_circuit(self, operation: LogicalOperation):
        if operation.gate == LogicalGateLabel.X:
            return Circuit(X(self.data_qubits[operation.qubit_index]))
        elif operation.gate == LogicalGateLabel.Z:
            return Circuit(Z(self.data_qubits[operation.qubit_index]))
        return None
