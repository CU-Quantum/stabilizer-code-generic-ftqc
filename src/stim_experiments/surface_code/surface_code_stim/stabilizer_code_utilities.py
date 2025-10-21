import numpy as np
from numpy._typing import NDArray
from stim import Circuit


class StabilizerCodeUtilities:
    def __init__(self,
                 symplectic_matrix: NDArray[NDArray[int]],
                 generator_anticommutors: NDArray[NDArray[int]],
                 qubit_id_start: int = 0,
                 row_coord_start: int = 0,):
        self._symplectic_matrix = symplectic_matrix
        self._generator_anticommutors = generator_anticommutors
        self._qubit_id_start = qubit_id_start
        self.row_coord_start = row_coord_start

    def get_init(self):
        anticommutor_circuit = Circuit()
        for ancilla_index, anticommutor in zip(self.ancilla_indices, self._generator_anticommutors):
            self.apply_stabilizer(anticommutor, anticommutor_circuit, ancilla_index)

        return Circuit(f"""
            {'\n'.join([f'QUBIT_COORDS({self.row_coord_start}, {i}) {q_index}' for i, q_index in enumerate(self.data_indices)])}
            {'\n'.join([f'QUBIT_COORDS({self.row_coord_start + 1}, {i}) {q_index}' for i, q_index in enumerate(self.ancilla_indices)])}
            R {' '.join(map(str, self.data_indices))}
            R {' '.join(map(str, self.ancilla_indices))}
            
            {self.get_stabilizers()}

            M {' '.join(map(str, self.ancilla_indices))}
            {anticommutor_circuit}
            R {' '.join(map(str, self.ancilla_indices))}
        """)

    def get_stabilizers(self) -> Circuit:
        circuit = Circuit()
        for ancilla_index, stabilizer in zip(self.ancilla_indices, self._symplectic_matrix):
            circuit.append('H', ancilla_index)
            self.apply_stabilizer(stabilizer, circuit, ancilla_index)
            circuit.append('H', ancilla_index)
        return circuit

    def apply_stabilizer(self, stabilizer, circuit, ancilla_index):
        x_qubits = np.argwhere(stabilizer[:len(self.data_indices)] == 1).flatten()
        z_qubits = np.argwhere(stabilizer[len(self.data_indices):] == 1).flatten()
        if len(x_qubits):
            circuit.append('CX', list(j for i in zip([ancilla_index] * len(x_qubits), np.array(self.data_indices)[x_qubits]) for j in i))
        if len(z_qubits):
            circuit.append('CZ', list(j for i in zip([ancilla_index] * len(z_qubits), np.array(self.data_indices)[z_qubits]) for j in i))

    @property
    def ancilla_indices(self) -> list[int]:
        num_ancillas = self._symplectic_matrix.shape[0]
        start_ancilla_index = self._qubit_id_start + len(self.data_indices)
        return list(range(start_ancilla_index, start_ancilla_index + num_ancillas))

    @property
    def data_indices(self) -> list[int]:
        num_data_qubits = self._symplectic_matrix.shape[1] // 2
        return list(range(self._qubit_id_start, self._qubit_id_start + num_data_qubits))
