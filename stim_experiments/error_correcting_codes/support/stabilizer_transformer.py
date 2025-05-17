from typing import List

from stim_experiments.custom_dataclasses.check_matrix import CheckMatrix
from stim_experiments.custom_dataclasses.transformation_operation import \
    TransformationGate, TransformationOperation


class StabilizerTransformer:
    def __init__(self, check_matrix: CheckMatrix):
        self._check_matrix = check_matrix

    def apply(self, operations: List[TransformationOperation]):
        for operation in operations:
            index_z_target = operation.target_qubit_index + self._check_matrix.num_physical_qubits
            index_z_control = None if operation.control_qubit_index is None else operation.control_qubit_index + self._check_matrix.num_physical_qubits
            for row in self._check_matrix.matrix:
                target_has_x_operator = row[operation.target_qubit_index]
                target_has_z_operator = row[index_z_target]
                control_has_x_operator = row[operation.control_qubit_index]
                control_has_z_operator = row[index_z_control]
                if operation.gate == TransformationGate.CX:
                    if control_has_x_operator:
                        row[operation.target_qubit_index] = (row[operation.target_qubit_index] + 1) % 2
                    if target_has_z_operator:
                        row[index_z_control] = (row[index_z_control] + 1) % 2
                elif operation.gate == TransformationGate.CZ:
                    if control_has_x_operator:
                        row[index_z_control] = (row[index_z_control] + 1) % 2
                    if control_has_z_operator:
                        row[index_z_target] = (row[index_z_target] + 1) % 2 * row[index_z_control]
                        row[index_z_control] = 0
                elif operation.gate == TransformationGate.H:
                    if target_has_x_operator:
                        row[operation.target_qubit_index] = 0
                        row[index_z_target] = (row[index_z_target] + 1) % 2
                    if target_has_z_operator:
                        row[operation.target_qubit_index] = (row[operation.target_qubit_index] + 1) % 2
                        row[index_z_target] = 0
                elif operation.gate == TransformationGate.X:
                    if target_has_z_operator:
                        row[index_z_target] *= -1
                elif operation.gate == TransformationGate.Z:
                    raise NotImplementedError


    def get_current_check_matrix(self) -> CheckMatrix:
        return self._check_matrix
