from dataclasses import dataclass
from functools import reduce
from typing import List, Optional

from cirq import CCX, CX, Circuit, DensityMatrixSimulator, DensityMatrixTrialResult, Gate, H, LineQubit, M, X, Z, \
    bit_flip, \
    kron

from stim_experiments.error_correcting_codes.error_correcting_code.error_correcting_code import ErrorCorrectingCode
from stim_experiments.utilities import DENSITY_MATRIX_TYPE, KET_ZERO_DENSITY_MATRIX


class ShorsRepetitionCode(ErrorCorrectingCode):
    def __init__(self, initial_qubit_state_density_matrix: DENSITY_MATRIX_TYPE):
        super().__init__(initial_qubit_state_density_matrix=initial_qubit_state_density_matrix)
        self._num_physical_qubits = 9
        self._num_ancillas_qubits = 2
        self._qubits = LineQubit.range(self._num_physical_qubits + self._num_ancillas_qubits)

        each_qubit_initial_state = ([self._initial_qubit_state_density_matrix]
                                    + [KET_ZERO_DENSITY_MATRIX for _ in range(len(self._qubits) - 1)])
        self._current_state = reduce(kron, each_qubit_initial_state)
        self._current_state = self._encode_logical_qubit()

    def _encode_logical_qubit(self) -> DENSITY_MATRIX_TYPE:
        outer_qubits_indices = list(range(0, self._num_physical_qubits, 3))
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

    def correct_bit_flips(self) -> None:
        for i in range(3):
            self._correct_bit_flip(block_number=i)

    def _correct_bit_flip(self, block_number: int) -> None:
        ancillas = self._qubits[self._num_physical_qubits:]
        circuit = Circuit(
            [CX(self._qubits[i], ancillas[0]) for i in range(3 * block_number + 2)],
            [CX(self._qubits[i], ancillas[1]) for i in range(3 * block_number + 1, 3 * block_number + 3)],
            [M(ancilla) for ancilla in ancillas],
            X.controlled(num_controls=2, control_values=[0,1]).on(ancillas[0], ancillas[1], self._qubits[2]),
            X.controlled(num_controls=2, control_values=[1,0]).on(ancillas[0], ancillas[1], self._qubits[0]),
            X.controlled(num_controls=2, control_values=[1,1]).on(ancillas[0], ancillas[1], self._qubits[1]),
        )
        self._current_state = self._get_state_after_circuit(circuit=circuit)

    def get_current_state(self, qubit_indices: Optional[List[int]] = None) -> DENSITY_MATRIX_TYPE:
        physical_qubit_indices = qubit_indices or list(range(self._num_physical_qubits))
        return super().get_current_state(qubit_indices=physical_qubit_indices)
