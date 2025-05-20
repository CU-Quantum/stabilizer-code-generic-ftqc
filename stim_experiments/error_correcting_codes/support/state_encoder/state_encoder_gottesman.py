from typing import List

from cirq import Circuit, Gate, H, LineQubit, Operation

from stim_experiments.custom_dataclasses.check_matrix import CheckMatrix, \
    TYPE_CHECK_MATRIX
from stim_experiments.custom_dataclasses.check_matrix_standardized import \
    CheckMatrixStandardized
from stim_experiments.custom_dataclasses.state_encoding import StateEncoding
from stim_experiments.error_correcting_codes.support.check_matrix_to_gates import \
    CheckMatrixToGates
from stim_experiments.error_correcting_codes.support.state_encoder.state_encoder import StateEncoder


class StateEncoderGottesman(StateEncoder):
    def __init__(self, check_matrix_standardized: CheckMatrixStandardized, data_qubits: list[LineQubit]):
        super().__init__(check_matrix=check_matrix_standardized, data_qubits=data_qubits)
        self._check_matrix_standardized = check_matrix_standardized

    def get_encoding_circuit(self) -> StateEncoding:
        hadamards = [H(self._get_qubit_at_index(control_index)) for control_index in
                     range(self._check_matrix_standardized.rank_of_pauli_x_portion)]
        return StateEncoding(
            circuit=Circuit(
                self._encode_logical_nots(),
                zip(hadamards, self._encode_generators()),
            )
        )

    def _encode_logical_nots(self) -> List[List[List[Operation]]]:
        return [self._get_controlled_gates(matrix_form_gates=self._check_matrix_standardized.logical_xs,
                                           control_num=control_num,
                                           control_index=self._check_matrix_standardized.num_physical_qubits - self._check_matrix_standardized.num_logical_qubits + control_num)
                for control_num in range(self._check_matrix_standardized.num_logical_qubits)]

    def _encode_generators(self) -> List[List[List[Operation]]]:
        return [self._get_controlled_gates(matrix_form_gates=self._check_matrix_standardized.matrix,
                                           control_num=control_num,
                                           control_index=control_num)
                for control_num in range(self._check_matrix_standardized.rank_of_pauli_x_portion)]

    def _get_controlled_gates(self, matrix_form_gates: TYPE_CHECK_MATRIX, control_num: int, control_index: int) -> List[List[Operation]]:
        controlled_gates = CheckMatrixToGates(check_matrix=CheckMatrix(matrix=matrix_form_gates)).get_gates()
        return [self._get_controlled_gates_at_qubit(gates=gates, control_index=control_index, target_index=target_index)
                for target_index, gates in enumerate(controlled_gates[control_num])]

    def _get_controlled_gates_at_qubit(self, gates: List[Gate], control_index: int, target_index: int) -> List[Operation]:
        control_qubit = self._get_qubit_at_index(control_index)
        target_qubit = self._get_qubit_at_index(target_index)
        operations = [gate(target_qubit) for gate in gates[target_qubit == control_qubit:]]  # ignores x gate in control qubit
        return [operation if target_qubit == control_qubit else operation.controlled_by(control_qubit) for operation in operations]

    def _get_qubit_at_index(self, qubit_index: int) -> LineQubit:
        return self._data_qubits[qubit_index]
