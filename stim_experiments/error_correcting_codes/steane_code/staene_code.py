from functools import reduce

from cirq import CX, CZ, Circuit, H, R, kron

from stim_experiments.error_correcting_codes.error_correcting_code.error_correcting_code import ErrorCorrectingCode
from stim_experiments.utilities import DENSITY_MATRIX_TYPE, KET_ZERO_DENSITY_MATRIX


class SteaneCode(ErrorCorrectingCode):
    def __init__(self, initial_qubit_state_density_matrix: DENSITY_MATRIX_TYPE):
        super().__init__(initial_qubit_state_density_matrix=initial_qubit_state_density_matrix, num_data_qubits=7, num_ancilla_qubits=6)

        each_qubit_initial_state = ([self._initial_qubit_state_density_matrix]
                                    + [KET_ZERO_DENSITY_MATRIX for _ in range(len(self._qubits) - 1)])
        self._current_state = reduce(kron, each_qubit_initial_state)
        self._current_state = self._encode_logical_qubit()

    def _encode_logical_qubit(self) -> DENSITY_MATRIX_TYPE:
        stabilizer_indices_x = [(0, 4, 5, 6), (1, 3, 5, 6), (2, 3, 4, 5)]
        stabilizer_indices_z = [(0, 2, 3, 6), (1, 2, 4, 6), (0, 1, 2, 5)]
        circuit = Circuit(
            [CX(self._qubits[0], qubit) for qubit in self._data_qubits[1:]],
            [H(ancilla) for ancilla in self._ancilla_qubits],
            [CX(self._ancilla_qubits[ancilla_index], self._data_qubits[data_index])
             for ancilla_index, data_indices in enumerate(stabilizer_indices_x)
             for data_index in data_indices],
            [CZ(self._ancilla_qubits[ancilla_index + len(stabilizer_indices_x)], self._data_qubits[data_index])
             for ancilla_index, data_indices in enumerate(stabilizer_indices_z)
             for data_index in data_indices],
            [H(ancilla) for ancilla in self._ancilla_qubits],
            [R(ancilla) for ancilla in self._ancilla_qubits],
        )

        return self._get_state_after_circuit(circuit=circuit)

    def correct_errors(self):
        pass
