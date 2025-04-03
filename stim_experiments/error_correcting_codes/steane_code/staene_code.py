from typing import List

from cirq import CX, CZ, Circuit, DensityMatrixSimulator, DensityMatrixTrialResult, Gate, H, R, X, Z, kron

from stim_experiments.error_correcting_codes.error_correcting_code.error_correcting_code import ErrorCorrectingCode
from stim_experiments.utilities import DENSITY_MATRIX_TYPE, KET_ZERO_DENSITY_MATRIX


class SteaneCode(ErrorCorrectingCode):
    _stabilizer_indices = [(3, 4, 5, 6), (1, 2, 5, 6), (0, 2, 4, 6)]

    def __init__(self, initial_logical_qubit_state_density_matrix: DENSITY_MATRIX_TYPE):
        super().__init__(initial_logical_qubit_state_density_matrix=initial_logical_qubit_state_density_matrix, num_data_qubits=7, num_ancilla_qubits=3)

    def _encode_logical_qubit(self) -> None:
        initial_state = kron(self._initial_logical_qubit_state_density_matrix, *[KET_ZERO_DENSITY_MATRIX] * (len(self._qubits) - 1))
        initialize_with_given_state = Circuit(
            [CX(self._data_qubits[0], data_qubit) for data_qubit in self._data_qubits[1:]],
        )
        initial_state_simulation: DensityMatrixTrialResult = DensityMatrixSimulator().simulate(initialize_with_given_state,
                                                                                               qubit_order=self._qubits,
                                                                                               initial_state=initial_state)
        self._current_state = initial_state_simulation.final_density_matrix

        self.correct_errors()

    def correct_errors(self) -> None:
        self._correct_bit_flips()
        self._correct_phase_flips()

    def _correct_bit_flips(self) -> None:
        syndrome = Circuit(
            [CX(self._data_qubits[data_index], self._ancilla_qubits[ancilla_index])
             for ancilla_index, data_indices in enumerate(self._stabilizer_indices)
             for data_index in data_indices],
        )
        self._correct_error(syndrome=syndrome, correction_gate=X)

    def _correct_phase_flips(self) -> None:
        syndrome = Circuit(
            [H(ancilla) for ancilla in self._ancilla_qubits],
            [CX(self._ancilla_qubits[ancilla_index], self._data_qubits[data_index])
             for ancilla_index, data_indices in enumerate(self._stabilizer_indices)
             for data_index in data_indices],
            [H(ancilla) for ancilla in self._ancilla_qubits],
        )
        self._correct_error(syndrome=syndrome, correction_gate=Z)

    def _correct_error(self, syndrome: Circuit, correction_gate: Gate) -> None:
        recovery = Circuit(
            [correction_gate.controlled(num_controls=3, control_values=self._get_binary_array_for_ancillas(i + 1)).on(
                self._ancilla_qubits[0],
                self._ancilla_qubits[1],
                self._ancilla_qubits[2],
                self._data_qubits[i]
            ) for i in range(self._num_data_qubits)]
        )
        circuit = Circuit(
            syndrome,
            recovery,
            [R(ancilla) for ancilla in self._ancilla_qubits],
        )
        self._current_state = self._get_state_after_circuit(circuit=circuit)

    def _get_binary_array_for_ancillas(self, num: int) -> List[int]:
        return list(map(int, bin(num)[2:].rjust(self._num_ancilla_qubits, '0')))
