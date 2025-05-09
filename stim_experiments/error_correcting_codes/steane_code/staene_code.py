from typing import Optional

from cirq import CX, Circuit, DensityMatrixSimulator, DensityMatrixTrialResult, Gate, H, LineQubit, R, X, Z

from stim_experiments.error_correcting_codes.error_correcting_code.error_correcting_code import ErrorCorrectingCode
from stim_experiments.custom_dataclasses.logical_operation import LogicalGateLabel, LogicalOperation
from stim_experiments.utilities import KET_ZERO_DENSITY_MATRIX, \
    TYPE_STATE_VECTOR_OR_DENSITY_MATRIX, int_to_binary_array, tensor


class SteaneCode(ErrorCorrectingCode):
    _stabilizer_indices = [(3, 4, 5, 6), (1, 2, 5, 6), (0, 2, 4, 6)]

    def __init__(self,
                 qubit_start_index: int = 0,
                 provided_ancilla_qubits: Optional[list[LineQubit]] = None, ):
        super().__init__(num_data_qubits=7,
                         num_ancilla_qubits=3,
                         num_logical_qubits=1,
                         qubit_start_index=qubit_start_index,
                         provided_ancilla_qubits=provided_ancilla_qubits)

    def encode_logical_qubit(self) -> TYPE_STATE_VECTOR_OR_DENSITY_MATRIX:
        return self.get_error_correction_circuit(),

    def _perform_get_operation_circuit(self, operation: LogicalOperation) -> None:
        pass

    @property
    def _implemented_operations(self) -> list[LogicalGateLabel]:
        return []

    def get_error_correction_circuit(self) -> Circuit:
        return Circuit(
            self._correct_bit_flips(),
            self._correct_phase_flips()
        )

    def _correct_bit_flips(self) -> Circuit:
        syndrome = Circuit(
            [CX(self.data_qubits[data_index], self.ancilla_qubits[ancilla_index])
             for ancilla_index, data_indices in enumerate(self._stabilizer_indices)
             for data_index in data_indices],
        )
        return self._correct_error(syndrome=syndrome, correction_gate=X)

    def _correct_phase_flips(self) -> Circuit:
        syndrome = Circuit(
            [H(ancilla) for ancilla in self.ancilla_qubits],
            [CX(self.ancilla_qubits[ancilla_index], self.data_qubits[data_index])
             for ancilla_index, data_indices in enumerate(self._stabilizer_indices)
             for data_index in data_indices],
            [H(ancilla) for ancilla in self.ancilla_qubits],
        )
        return self._correct_error(syndrome=syndrome, correction_gate=Z)

    def _correct_error(self, syndrome: Circuit, correction_gate: Gate) -> Circuit:
        recovery = Circuit(
            [correction_gate.controlled(num_controls=3, control_values=int_to_binary_array(num=i + 1, num_elements=self._num_ancilla_qubits)).on(
                *self.ancilla_qubits,
                self.data_qubits[i]
            ) for i in range(self._num_data_qubits)]
        )
        circuit = Circuit(
            syndrome,
            recovery,
            [R(ancilla) for ancilla in self.ancilla_qubits],
        )
        return circuit
