import numpy as np
import stim
from numpy._typing import NDArray


def get_stabilizer_code_line(symplectic_matrix: NDArray[NDArray[int]], qubit_id_start: int = 0):
    num_data_qubits = symplectic_matrix.shape[1] // 2
    num_ancillas = symplectic_matrix.shape[0]
    data_qubit_indices = list(range(qubit_id_start, qubit_id_start + num_data_qubits))
    ancilla_qubit_indices = list(range(qubit_id_start + num_data_qubits, qubit_id_start + num_data_qubits + num_ancillas))
    circuit = stim.Circuit()
    for i, stabilizer in enumerate(symplectic_matrix):
        x_qubits = np.argwhere(stabilizer[:num_data_qubits] == 1).flatten()
        z_qubits = np.argwhere(stabilizer[num_data_qubits:] == 1).flatten()
        circuit.append('H', ancilla_qubit_indices[i])
        circuit.append('CX', list(j for i in zip([ancilla_qubit_indices[i]] * len(x_qubits), np.array(data_qubit_indices)[x_qubits]) for j in i))
        circuit.append('CZ', list(j for i in zip([ancilla_qubit_indices[i]] * len(z_qubits), np.array(data_qubit_indices)[z_qubits]) for j in i))
        circuit.append('H', ancilla_qubit_indices[i])
    return circuit
