from functools import reduce

from cirq import CX, CZ, Circuit, DensityMatrixSimulator, H, M, R, X, Z, kron

from stim_experiments.error_correcting_codes.error_correcting_code.error_correcting_code import ErrorCorrectingCode
from stim_experiments.utilities import DENSITY_MATRIX_TYPE


class SteaneCodeUtilities:
    def get_logical_hadamard(self) -> DENSITY_MATRIX_TYPE:
        circuit = Circuit(
            [CX(self._qubits[0], qubit) for qubit in self._data_qubits[1:]],
            [H(data_qubit) for data_qubit in self._data_qubits],
        )
        self._current_state = self._get_state_after_circuit(circuit=circuit)


class SteaneCode(ErrorCorrectingCode):
    def __init__(self, initial_logical_qubit_state_density_matrix: DENSITY_MATRIX_TYPE):
        super().__init__(initial_logical_qubit_state_density_matrix=initial_logical_qubit_state_density_matrix, num_data_qubits=7, num_ancilla_qubits=6)

    def _encode_logical_qubit(self) -> None:
        circuit = Circuit(
            H(self._data_qubits[0]),
            H(self._data_qubits[1]),
            H(self._data_qubits[3]),

            CX(self._data_qubits[0], self._data_qubits[2]),
            CX(self._data_qubits[3], self._data_qubits[5]),

            CX(self._data_qubits[1], self._data_qubits[6]),
            CX(self._data_qubits[0], self._data_qubits[4]),
            CX(self._data_qubits[3], self._data_qubits[6]),
            CX(self._data_qubits[1], self._data_qubits[5]),
            CX(self._data_qubits[0], self._data_qubits[6]),

            CX(self._data_qubits[1], self._data_qubits[2]),
            CX(self._data_qubits[3], self._data_qubits[4]),
        )
        self._current_state = self._get_state_after_circuit(circuit=circuit)


    def correct_errors(self) -> None:
        stabilizer_indices_x = [(0, 4, 5, 6), (1, 3, 5, 6), (2, 3, 4, 5)]
        stabilizer_indices_z = [(0, 2, 3, 6), (1, 2, 4, 6), (0, 1, 2, 5)]
        syndrome = Circuit(
            [H(ancilla) for ancilla in self._ancilla_qubits],
            [CX(self._ancilla_qubits[ancilla_index], self._data_qubits[data_index])
             for ancilla_index, data_indices in enumerate(stabilizer_indices_x)
             for data_index in data_indices],
            [CZ(self._ancilla_qubits[ancilla_index + len(stabilizer_indices_x)], self._data_qubits[data_index])
             for ancilla_index, data_indices in enumerate(stabilizer_indices_z)
             for data_index in data_indices],
            [H(ancilla) for ancilla in self._ancilla_qubits],
        )

        recovery_z = Circuit(
            Z.controlled(num_controls=3, control_values=[0, 0, 1]).on(
                self._ancilla_qubits[0],
                self._ancilla_qubits[1],
                self._ancilla_qubits[2],
                self._data_qubits[2]
            ),
            Z.controlled(num_controls=3, control_values=[0, 1, 0]).on(
                self._ancilla_qubits[0],
                self._ancilla_qubits[1],
                self._ancilla_qubits[2],
                self._data_qubits[1]
            ),
            Z.controlled(num_controls=3, control_values=[0, 1, 1]).on(
                self._ancilla_qubits[0],
                self._ancilla_qubits[1],
                self._ancilla_qubits[2],
                self._data_qubits[3]
            ),
            Z.controlled(num_controls=3, control_values=[1, 0, 0]).on(
                self._ancilla_qubits[0],
                self._ancilla_qubits[1],
                self._ancilla_qubits[2],
                self._data_qubits[0]
            ),
            Z.controlled(num_controls=3, control_values=[1, 0, 1]).on(
                self._ancilla_qubits[0],
                self._ancilla_qubits[1],
                self._ancilla_qubits[2],
                self._data_qubits[4]
            ),
            Z.controlled(num_controls=3, control_values=[1, 1, 0]).on(
                self._ancilla_qubits[0],
                self._ancilla_qubits[1],
                self._ancilla_qubits[2],
                self._data_qubits[6]
            ),
            Z.controlled(num_controls=3, control_values=[1, 1, 1]).on(
                self._ancilla_qubits[0],
                self._ancilla_qubits[1],
                self._ancilla_qubits[2],
                self._data_qubits[5]
            ),
        )

        recovery_x = Circuit(
            X.controlled(num_controls=3, control_values=[0, 0, 1]).on(
                self._ancilla_qubits[3],
                self._ancilla_qubits[4],
                self._ancilla_qubits[5],
                self._data_qubits[5]
            ),
            X.controlled(num_controls=3, control_values=[0, 1, 0]).on(
                self._ancilla_qubits[3],
                self._ancilla_qubits[4],
                self._ancilla_qubits[5],
                self._data_qubits[4]
            ),
            X.controlled(num_controls=3, control_values=[0, 1, 1]).on(
                self._ancilla_qubits[3],
                self._ancilla_qubits[4],
                self._ancilla_qubits[5],
                self._data_qubits[1]
            ),
            X.controlled(num_controls=3, control_values=[1, 0, 0]).on(
                self._ancilla_qubits[3],
                self._ancilla_qubits[4],
                self._ancilla_qubits[5],
                self._data_qubits[3]
            ),
            X.controlled(num_controls=3, control_values=[1, 0, 1]).on(
                self._ancilla_qubits[3],
                self._ancilla_qubits[4],
                self._ancilla_qubits[5],
                self._data_qubits[0]
            ),
            X.controlled(num_controls=3, control_values=[1, 1, 0]).on(
                self._ancilla_qubits[3],
                self._ancilla_qubits[4],
                self._ancilla_qubits[5],
                self._data_qubits[6]
            ),
            X.controlled(num_controls=3, control_values=[1, 1, 1]).on(
                self._ancilla_qubits[3],
                self._ancilla_qubits[4],
                self._ancilla_qubits[5],
                self._data_qubits[2]
            ),
        )

        circuit = Circuit(
            syndrome,
            recovery_z,
            recovery_x,
            [R(ancilla) for ancilla in self._ancilla_qubits],
        )
        self._current_state = self._get_state_after_circuit(circuit=circuit)
