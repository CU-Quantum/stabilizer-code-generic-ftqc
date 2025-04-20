from typing import List

from cirq import Circuit, X, Z

from stim_experiments.custom_dataclasses.logical_operation import LogicalGateLabel, LogicalOperation
from stim_experiments.error_correcting_codes.error_correcting_code.error_correcting_code import ErrorCorrectingCode
from stim_experiments.utilities import KET_ZERO_STATE_VECTOR, TYPE_STATE_VECTOR_OR_DENSITY_MATRIX


class ErrorCorrectingCodeStub(ErrorCorrectingCode):
    def __init__(self, qubit_start_index: int = 0):
        super().__init__(num_data_qubits=1,
                         num_ancilla_qubits=0,
                         num_logical_qubits=1,
                         initial_logical_qubit_state=KET_ZERO_STATE_VECTOR,
                         qubit_start_index=qubit_start_index)

    def encode_logical_qubit(self) -> TYPE_STATE_VECTOR_OR_DENSITY_MATRIX:
        return self._initial_logical_qubit_state

    def get_error_correction_circuit(self) -> Circuit:
        pass

    def _perform_get_operation_circuit(self, operation: LogicalOperation) -> Circuit:
        if operation.gate == LogicalGateLabel.X:
            return Circuit(X(self.data_qubits[0]))
        else:
            return Circuit(Z(self.data_qubits[0]))

    @property
    def _implemented_operations(self) -> List[LogicalGateLabel]:
        return [LogicalGateLabel.X, LogicalGateLabel.Z]
