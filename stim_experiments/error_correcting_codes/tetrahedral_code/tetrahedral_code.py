from typing import Optional

from cirq import Circuit, LineQubit, Operation

from stim_experiments.custom_dataclasses.check_matrix import CheckMatrix
from stim_experiments.custom_dataclasses.logical_operation import LogicalOperation
from stim_experiments.error_correcting_codes.stabilizer_code.stabilizer_code import StabilizerCode
from stim_experiments.utilities.predefined_check_matrix_values import get_check_matrix_values_tetrahedral


class TetrahedralCode(StabilizerCode):
    def __init__(self, qubits: Optional[list[LineQubit]] = None):
        check_matrix = CheckMatrix(matrix=get_check_matrix_values_tetrahedral())
        super().__init__(check_matrix=check_matrix, qubits=qubits)

    def _get_anticommuter_for_generator(self, generator_index: int) -> list[Operation]:
        pass

    def _perform_get_operation_circuit(self, operation: LogicalOperation) -> Optional[Circuit]:
        pass
