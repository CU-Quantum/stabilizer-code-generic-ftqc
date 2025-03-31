from functools import reduce

from cirq import CX, Circuit, DensityMatrixSimulator, DensityMatrixTrialResult, H, LineQubit, kron

from stim_experiments.error_correcting_codes.error_correcting_code.error_correcting_code import ErrorCorrectingCode
from stim_experiments.utilities import DENSITY_MATRIX_TYPE, KET_ZERO_DENSITY_MATRIX


class ShorsRepetitionCode(ErrorCorrectingCode):
    def __init__(self, initial_qubit_state_density_matrix: DENSITY_MATRIX_TYPE):
        super().__init__()
        self._current_state = self._encode_initial_state(initial_qubit_state_density_matrix)

    def _encode_initial_state(self, initial_state: DENSITY_MATRIX_TYPE) -> DENSITY_MATRIX_TYPE:
        num_physical_qubits = 9
        qubits = LineQubit.range(num_physical_qubits)
        outer_qubits_indices = list(range(0, num_physical_qubits, 3))
        outer_qubits = [qubits[i] for i in outer_qubits_indices]
        circuit = Circuit(
            [CX(outer_qubits[0], target_qubit) for target_qubit in outer_qubits[1:]],
            [H(target_qubit) for target_qubit in outer_qubits],
            [CX(qubits[control_qubit_index], qubits[control_qubit_index + i + 1])
             for control_qubit_index in outer_qubits_indices
             for i in range(2)],
        )

        each_qubit_initial_state = [initial_state] + [KET_ZERO_DENSITY_MATRIX for _ in range(num_physical_qubits - 1)]
        initial_state = reduce(kron, each_qubit_initial_state)
        simulation: DensityMatrixTrialResult = DensityMatrixSimulator().simulate(circuit, qubit_order=qubits, initial_state=initial_state)
        return simulation.final_density_matrix
