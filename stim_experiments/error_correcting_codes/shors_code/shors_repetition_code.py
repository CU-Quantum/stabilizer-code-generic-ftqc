from typing import Optional

from cirq import CX, Circuit, H, LineQubit, R, X, Z

from stim_experiments.error_correcting_codes.error_correcting_code.error_correcting_code import ErrorCorrectingCode
from stim_experiments.custom_dataclasses.logical_operation import LogicalGateLabel, LogicalOperation
from stim_experiments.utilities import KET_ZERO_DENSITY_MATRIX, TYPE_STATE_VECTOR_OR_DENSITY_MATRIX, tensor


class ShorsRepetitionCode(ErrorCorrectingCode):
    def __init__(self,
                 qubit_start_index: int = 0,
                 provided_ancilla_qubits: Optional[list[LineQubit]] = None, ):
        super().__init__(num_data_qubits=9,
                         num_ancilla_qubits=2,
                         num_logical_qubits=1,
                         qubit_start_index=qubit_start_index,
                         provided_ancilla_qubits=provided_ancilla_qubits)

    def encode_logical_qubit(self) -> Circuit:
        outer_qubits_indices = list(range(0, self._num_data_qubits, 3))
        outer_qubits = [self.all_qubits[i] for i in outer_qubits_indices]
        return Circuit(
            [CX(outer_qubits[0], target_qubit) for target_qubit in outer_qubits[1:]],
            [H(target_qubit) for target_qubit in outer_qubits],
            [CX(self.all_qubits[control_qubit_index], self.all_qubits[control_qubit_index + i + 1])
             for control_qubit_index in outer_qubits_indices
             for i in range(2)],
        )

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

    def _correct_bit_flips(self) -> list[Circuit]:
        return [self._correct_bit_flip(block_number=i) for i in range(3)]

    def _correct_bit_flip(self, block_number: int) -> Circuit:
        block_start_index = 3 * block_number
        syndrome = Circuit(
            [CX(self.all_qubits[i], self.ancilla_qubits[0]) for i in range(block_start_index, block_start_index + 2)],
            [CX(self.all_qubits[i], self.ancilla_qubits[1]) for i in range(block_start_index + 1, block_start_index + 3)],
        )
        correction = Circuit(
            X.controlled(num_controls=2, control_values=[0,1]).on(self.ancilla_qubits[0], self.ancilla_qubits[1], self.all_qubits[block_start_index + 2]),
            X.controlled(num_controls=2, control_values=[1,0]).on(self.ancilla_qubits[0], self.ancilla_qubits[1], self.all_qubits[block_start_index]),
            X.controlled(num_controls=2, control_values=[1,1]).on(self.ancilla_qubits[0], self.ancilla_qubits[1], self.all_qubits[block_start_index + 1]),
        )
        circuit = Circuit(
            syndrome,
            correction,
            [R(ancilla) for ancilla in self.ancilla_qubits],
        )
        return circuit

    def _correct_phase_flips(self) -> Circuit:
        syndrome = Circuit(
            [H(ancilla) for ancilla in self.ancilla_qubits],
            [CX(self.ancilla_qubits[0], self.all_qubits[i]) for i in range(6)],
            [CX(self.ancilla_qubits[1], self.all_qubits[i]) for i in range(3, 9)],
            [H(ancilla) for ancilla in self.ancilla_qubits],
        )
        correction = Circuit(
            [Z.controlled(num_controls=2, control_values=[0, 1]).on(self.ancilla_qubits[0], self.ancilla_qubits[1], self.all_qubits[i]) for i in range(6, 9)],
            [Z.controlled(num_controls=2, control_values=[1, 0]).on(self.ancilla_qubits[0], self.ancilla_qubits[1], self.all_qubits[i]) for i in range(3)],
            [Z.controlled(num_controls=2, control_values=[1, 1]).on(self.ancilla_qubits[0], self.ancilla_qubits[1], self.all_qubits[i]) for i in range(3, 6)],
        )
        circuit = Circuit(
            syndrome,
            correction,
            [R(ancilla) for ancilla in self.ancilla_qubits],
        )
        return circuit
