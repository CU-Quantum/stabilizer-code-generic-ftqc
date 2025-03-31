from functools import reduce

from cirq import CX, Circuit, DensityMatrixSimulator, DensityMatrixTrialResult, H, LineQubit, X, kron

from stim_experiments.error_correcting_codes.error_correcting_code.error_correcting_code import ErrorCorrectingCode
from stim_experiments.utilities import DENSITY_MATRIX_TYPE, KET_ZERO_DENSITY_MATRIX


class ShorsRepetitionCode(ErrorCorrectingCode):

    def __init__(self, initial_qubit_state_density_matrix: DENSITY_MATRIX_TYPE):
        super().__init__(initial_qubit_state_density_matrix=initial_qubit_state_density_matrix)
        self._num_physical_qubits = 9
        self._qubits = LineQubit.range(self._num_physical_qubits)

        each_qubit_initial_state = ([self._initial_qubit_state_density_matrix]
                                    + [KET_ZERO_DENSITY_MATRIX for _ in range(self._num_physical_qubits - 1)])
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

    def apply_bit_flip(self, qubit_index: int) -> None:
        circuit = Circuit(X(self._qubits[qubit_index]))
        self._current_state = self._get_state_after_circuit(circuit=circuit)

    def _get_state_after_circuit(self, circuit: Circuit) -> DENSITY_MATRIX_TYPE:
        simulator = DensityMatrixSimulator()
        simulation: DensityMatrixTrialResult = simulator.simulate(circuit, qubit_order=self._qubits, initial_state=self._current_state)
        return simulation.final_density_matrix
