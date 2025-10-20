import numpy as np
import stim
from numpy._typing import NDArray


def get_stabilizer_code_line(symplectic_matrix: NDArray[NDArray[int]], qubit_id_start: int = 0):
    num_data_qubits = symplectic_matrix.shape[1]
    num_ancillas = symplectic_matrix.shape[0]
    data_qubit_indices = list(range(qubit_id_start, qubit_id_start + num_data_qubits))
    ancilla_qubit_indices = list(range(qubit_id_start + num_data_qubits, qubit_id_start + num_data_qubits + num_ancillas))
    circuit = stim.Circuit()
    circuit.append('R', data_qubit_indices)
    circuit.append('R', ancilla_qubit_indices)
    for i, stabilizer in enumerate(symplectic_matrix):
        x_qubits = np.argwhere(stabilizer[:num_data_qubits // 2] == 1).flatten()
        circuit.append('H', ancilla_qubit_indices[i])
        circuit.append('CX', x_qubits)
        circuit.append('H', ancilla_qubit_indices[i])

        z_qubits = np.argwhere(stabilizer[num_data_qubits // 2:] == 1).flatten()
        circuit.append('H', ancilla_qubit_indices[i])
        circuit.append('CZ', z_qubits)
        circuit.append('H', ancilla_qubit_indices[i])
    circuit.append('M', ancilla_qubit_indices)
    for i in range(num_ancillas):
        circuit.append(f"DETECTOR rec[{-(num_ancillas-i)}]")
    return circuit
