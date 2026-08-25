from typing import Optional

from cirq import Circuit, LineQubit, Operation, X, Z

from cirq_experiments.custom_dataclasses.check_matrix import CheckMatrix
from cirq_experiments.custom_dataclasses.logical_operation import LogicalGateLabel, LogicalOperation
from cirq_experiments.error_correcting_codes.stabilizer_code.stabilizer_code import StabilizerCode
from predefined_check_matrix_values import get_check_matrix_values_golay


class GolayCode(StabilizerCode):
    def __init__(self, qubits: Optional[list[LineQubit]] = None):
        check_matrix = CheckMatrix(matrix=get_check_matrix_values_golay())
        super().__init__(check_matrix=check_matrix, qubits=qubits)

    def _get_anticommuter_for_generator(self, generator_index: int) -> list[Operation]:
        return [(Z if generator_index < 11 else X)(self.data_qubits[generator_index % 11])]

    def _perform_get_operation_circuit(self, operation: LogicalOperation) -> Optional[Circuit]:
        if operation.gate == LogicalGateLabel.X:
            return Circuit(
                [X(qubit) for qubit in self.data_qubits]
            )
        elif operation.gate == LogicalGateLabel.Z:
            return Circuit(
                [Z(qubit) for qubit in self.data_qubits]
            )
        return None
