from functools import reduce

from cirq import CX, Circuit, DensityMatrixSimulator, DensityMatrixTrialResult, Gate, H, I, LineQubit, M, R, X, Z, kron

from stim_experiments.error_correcting_codes.error_correcting_code.error_correcting_code import ErrorCorrectingCode
from stim_experiments.utilities import DENSITY_MATRIX_TYPE, KET_ZERO_DENSITY_MATRIX


class ShorsRepetitionCode(ErrorCorrectingCode):
    def __init__(self, initial_qubit_state_density_matrix: DENSITY_MATRIX_TYPE):
        super().__init__(initial_qubit_state_density_matrix=initial_qubit_state_density_matrix)
        self._num_data_qubits = 9
        self._num_ancillas_qubits = 2
        self._qubits = LineQubit.range(self._num_data_qubits + self._num_ancillas_qubits)
        self._data_qubits = self._qubits[:self._num_ancillas_qubits]
        self._ancilla_qubits = self._qubits[self._num_data_qubits:]

        each_qubit_initial_state = ([self._initial_qubit_state_density_matrix]
                                    + [KET_ZERO_DENSITY_MATRIX for _ in range(len(self._qubits) - 1)])
        self._current_state = reduce(kron, each_qubit_initial_state)
        self._current_state = self._encode_logical_qubit()

    def _encode_logical_qubit(self) -> DENSITY_MATRIX_TYPE:
        outer_qubits_indices = list(range(0, self._num_data_qubits, 3))
        outer_qubits = [self._qubits[i] for i in outer_qubits_indices]
        circuit = Circuit(
            [CX(outer_qubits[0], target_qubit) for target_qubit in outer_qubits[1:]],
            [H(target_qubit) for target_qubit in outer_qubits],
            [CX(self._qubits[control_qubit_index], self._qubits[control_qubit_index + i + 1])
             for control_qubit_index in outer_qubits_indices
             for i in range(2)],
        )

        return self._get_state_after_circuit(circuit=circuit)

    def apply_gate(self, gate: Gate, qubit_index: int) -> None:
        circuit = Circuit(gate(self._qubits[qubit_index]))
        self._current_state = self._get_state_after_circuit(circuit=circuit)

    def _get_state_after_circuit(self, circuit: Circuit) -> DENSITY_MATRIX_TYPE:
        simulator = DensityMatrixSimulator()
        simulation: DensityMatrixTrialResult = simulator.simulate(circuit, qubit_order=self._qubits, initial_state=self._current_state)
        return simulation.final_density_matrix

    def correct_errors(self):
        self._correct_bit_flips()
        self._correct_phase_flips()

    def _correct_bit_flips(self) -> None:
        for i in range(3):
            self._correct_bit_flip(block_number=i)

    def _correct_bit_flip(self, block_number: int) -> None:
        block_start_index = 3 * block_number
        syndrome = Circuit(
            [CX(self._qubits[i], self._ancilla_qubits[0]) for i in range(block_start_index, block_start_index + 2)],
            [CX(self._qubits[i], self._ancilla_qubits[1]) for i in range(block_start_index + 1, block_start_index + 3)],
        )
        correction = Circuit(
            X.controlled(num_controls=2, control_values=[0,1]).on(self._ancilla_qubits[0], self._ancilla_qubits[1], self._qubits[block_start_index + 2]),
            X.controlled(num_controls=2, control_values=[1,0]).on(self._ancilla_qubits[0], self._ancilla_qubits[1], self._qubits[block_start_index]),
            X.controlled(num_controls=2, control_values=[1,1]).on(self._ancilla_qubits[0], self._ancilla_qubits[1], self._qubits[block_start_index + 1]),
        )
        circuit = Circuit(
            syndrome,
            correction,
            [R(ancilla) for ancilla in self._ancilla_qubits],
        )
        self._current_state = self._get_state_after_circuit(circuit=circuit)

    def _correct_phase_flips(self):
        syndrome = Circuit(
            [H(ancilla) for ancilla in self._ancilla_qubits],
            [CX(self._ancilla_qubits[0], self._qubits[i]) for i in range(6)],
            [CX(self._ancilla_qubits[1], self._qubits[i]) for i in range(3, 9)],
            [H(ancilla) for ancilla in self._ancilla_qubits],
        )
        correction = Circuit(
            [Z.controlled(num_controls=2, control_values=[0, 1]).on(self._ancilla_qubits[0], self._ancilla_qubits[1], self._qubits[i]) for i in range(6, 9)],
            [Z.controlled(num_controls=2, control_values=[1, 0]).on(self._ancilla_qubits[0], self._ancilla_qubits[1], self._qubits[i]) for i in range(3)],
            [Z.controlled(num_controls=2, control_values=[1, 1]).on(self._ancilla_qubits[0], self._ancilla_qubits[1], self._qubits[i]) for i in range(3, 6)],
        )
        circuit = Circuit(
            syndrome,
            correction,
            [R(ancilla) for ancilla in self._ancilla_qubits],
        )
        self._current_state = self._get_state_after_circuit(circuit=circuit)
