import numpy as np
from numpy._typing import NDArray
from stim import Circuit

from generalized_shor_code_generators import GeneralizedShorCodeGenerators
from predefined_check_matrix_values import get_check_matrix_values_5_qubit, get_check_matrix_values_dodecacode, \
    get_check_matrix_values_tetrahedral


class StabilizerCodeUtilities:
    def __init__(self,
                 symplectic_matrix: NDArray[NDArray[int]],
                 generator_anticommutators: NDArray[NDArray[int]],
                 z_observable: NDArray[int],
                 x_observable: NDArray[int],
                 qubit_id_start: int = 0,
                 row_coord_start: int = 0,):
        self.symplectic_matrix = symplectic_matrix
        self.row_coord_start = row_coord_start
        self.z_observable = z_observable
        self.x_observable = x_observable

        self._generator_anticommutators = generator_anticommutators
        self._qubit_id_start = qubit_id_start

    def get_init(self):
        anticommutator_circuit = Circuit()
        for ancilla_index, anticommutator in zip(self.ancilla_indices, self._generator_anticommutators):
            self.apply_stabilizer(anticommutator, anticommutator_circuit, [ancilla_index] * self.num_measurement_ancillas)

        return Circuit(f"""
            {'\n'.join([f'QUBIT_COORDS({self.row_coord_start}, {i}) {q_index}' for i, q_index in enumerate(self.data_indices)])}
            {'\n'.join([f'QUBIT_COORDS({self.row_coord_start + 1}, {i}) {q_index}' for i, q_index in enumerate(self.all_ancilla_qubits)])}
            R {' '.join(map(str, self.data_indices))}
            R {' '.join(map(str, self.all_ancilla_qubits))}
        """)

    def get_encoding_by_stabilizer(self):
        anticommutator_circuit = Circuit()
        for ancilla_index, anticommutator in zip(self.ancilla_indices, self._generator_anticommutators):
            self.apply_stabilizer(anticommutator, anticommutator_circuit, [ancilla_index] * self.num_measurement_ancillas)

        return Circuit(f"""
            {self.get_stabilizers()}
            {anticommutator_circuit}
            R {' '.join(map(str, self.ancilla_indices))}
            
            {self._encode_z_observable()}
        """)

    def _encode_z_observable(self):
        ancilla_index = self.z_observable_ancilla
        circuit = Circuit()
        self.prepare_cat_state(ancilla_index, circuit)
        self.apply_stabilizer(self.z_observable, circuit, [ancilla_index] + self.measurement_ancillas)
        self.unprepare_cat_state(ancilla_index, circuit)
        circuit.append('M', ancilla_index)
        self.apply_stabilizer(self.x_observable, circuit, [ancilla_index] * self.num_measurement_ancillas)
        circuit.append('R', [ancilla_index] + self.measurement_ancillas)
        return circuit

    def get_stabilizers(self, modified_targets: list[int] = None, modified_ancilla: int = None) -> Circuit:
        circuit = Circuit()
        for ancilla_index, stabilizer in zip(self.ancilla_indices, self.symplectic_matrix):
            self.prepare_cat_state(ancilla_index, circuit)
            self.apply_stabilizer(stabilizer, circuit, [ancilla_index] + self.measurement_ancillas)
            if modified_targets and modified_ancilla == ancilla_index:
                circuit.append('CX', modified_targets)
            self.unprepare_cat_state(ancilla_index, circuit)
            circuit.append('M', ancilla_index)
            circuit.append('R', self.measurement_ancillas)
        return circuit

    def prepare_cat_state(self, ancilla_index: int, circuit: Circuit):
        circuit.append('H', ancilla_index)
        for measurement_index in self.measurement_ancillas:
            circuit.append('CX', [ancilla_index, measurement_index])

    def unprepare_cat_state(self, ancilla_index: int, circuit: Circuit):
        for measurement_index in self.measurement_ancillas:
            circuit.append('CX', [ancilla_index, measurement_index])
        circuit.append('H', ancilla_index)

    def apply_stabilizer(self, stabilizer, circuit, ancillas):
        x_qubits = np.argwhere(stabilizer[:len(self.data_indices)] == 1).flatten()
        z_qubits = np.argwhere(stabilizer[len(self.data_indices):] == 1).flatten()
        if len(x_qubits):
            circuit.append('CX', list(j for i in zip(ancillas, np.array(self.data_indices)[x_qubits]) for j in i))
        if len(z_qubits):
            circuit.append('CZ', list(j for i in zip(ancillas, np.array(self.data_indices)[z_qubits]) for j in i))

    @property
    def last_qubit_index(self):
        return self.measurement_ancillas[-1]

    @property
    def all_ancilla_qubits(self):
        return self.ancilla_indices + [self.z_observable_ancilla] + self.measurement_ancillas

    @property
    def measurement_ancillas(self):
        last_non_measurement_ancilla = self.z_observable_ancilla
        return list(range(last_non_measurement_ancilla + 1, last_non_measurement_ancilla + 1 + self.num_measurement_ancillas))

    @property
    def num_measurement_ancillas(self):
        return max(np.count_nonzero(self.z_observable), np.count_nonzero(self.x_observable), *np.count_nonzero(self.symplectic_matrix, axis=1))

    @property
    def z_observable_ancilla(self) -> int:
        return self.ancilla_indices[-1] + 1

    @property
    def ancilla_indices(self) -> list[int]:
        num_ancillas = self.symplectic_matrix.shape[0]
        start_ancilla_index = self._qubit_id_start + len(self.data_indices)
        return list(range(start_ancilla_index, start_ancilla_index + num_ancillas))

    @property
    def data_indices(self) -> list[int]:
        num_data_qubits = self.symplectic_matrix.shape[1] // 2
        return list(range(self._qubit_id_start, self._qubit_id_start + num_data_qubits))


def get_shor_h_observable_z(distance: int) -> NDArray:
    return np.concatenate([np.zeros(distance ** 2), *[np.concatenate([[1], np.zeros(distance - 1)])] * distance])


def get_shor_h_observable_x(distance: int) -> NDArray:
    return np.concatenate([np.ones(distance), np.zeros(distance * (distance - 1) + distance ** 2)])


def get_shor_code_utilities(num_cat_states: int,
                            num_qubits_per_cat_state: int,
                            z_observable: NDArray,
                            x_observable: NDArray,
                            qubit_id_start: int = 0,
                            row_coord_start: int = 0
                            ) -> StabilizerCodeUtilities:
    shor_code_generators = GeneralizedShorCodeGenerators(num_cats=num_cat_states, num_qubits_per_cat=num_qubits_per_cat_state)
    shor_code_symplectic_matrix = shor_code_generators.get_z_generators() + shor_code_generators.get_x_generators()
    shor_anticommutors = [
        np.concatenate(
            [np.ones(np.argmax(shor_code_symplectic_matrix[i][-len(shor_code_symplectic_matrix[0]) // 2 - 1:])),
             np.zeros(len(shor_code_symplectic_matrix[0]) - np.argmax(
                 shor_code_symplectic_matrix[i][-len(shor_code_symplectic_matrix[0]) // 2 - 1:]))])
        if i <= len(shor_code_symplectic_matrix) - num_cat_states
        else np.concatenate([np.zeros(len(shor_code_symplectic_matrix[0]) // 2), [
            int(not j % num_qubits_per_cat_state and j // num_qubits_per_cat_state < i - (
                        len(shor_code_symplectic_matrix) - num_cat_states)) for j in
            range(len(shor_code_symplectic_matrix[0]) // 2)]])
        for i in range(len(shor_code_symplectic_matrix))
    ]
    return StabilizerCodeUtilities(
        symplectic_matrix=np.array(shor_code_symplectic_matrix),
        generator_anticommutators=np.array(shor_anticommutors),
        z_observable=z_observable,
        x_observable=x_observable,
        qubit_id_start=qubit_id_start,
        row_coord_start=row_coord_start
    )


def get_15_1_3_reed_solomon_code_utilities():
    t_native_anticommutators = np.array([
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [1, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [1, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0],
    ])
    observable_z = np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
    observable_x = np.array([1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
    return StabilizerCodeUtilities(
        symplectic_matrix=get_check_matrix_values_tetrahedral(),
        generator_anticommutators=t_native_anticommutators,
        z_observable=observable_z,
        x_observable=observable_x
    )


def get_five_qubit_code_utilities():
    anticommutators = np.array([
        [0, 1, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 1, 1, 0, 0, 0, 0, 0, 0, 0],
        [0, 1, 1, 1, 0, 0, 0, 0, 0, 0],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    ])
    observable_z = np.array([0, 0, 0, 0, 0, 1, 1, 1, 1, 1])
    observable_x = np.array([1, 1, 1, 1, 1, 0, 0, 0, 0, 0])
    return StabilizerCodeUtilities(
        symplectic_matrix=get_check_matrix_values_5_qubit(),
        generator_anticommutators=anticommutators,
        z_observable=observable_z,
        x_observable=observable_x
    )


def get_3_repetition_code_utilities():
    symplectic_matrix = np.array([
        [0, 0, 0, 1, 1, 0],
        [0, 0, 0, 0, 1, 1],
    ])
    anticommutators = np.array([
        [1, 0, 0, 0, 0, 0],
        [0, 0, 1, 0, 0, 0],
    ])
    observable_z = np.array([0, 0, 0, 1, 1, 1])
    observable_x = np.array([1, 1, 1, 0, 0, 0])
    return StabilizerCodeUtilities(
        symplectic_matrix=symplectic_matrix,
        generator_anticommutators=anticommutators,
        z_observable=observable_z,
        x_observable=observable_x
    )


def get_dodecacode_utilities():
    symplectic_matrix = get_check_matrix_values_dodecacode()
    anticommutators = np.array([
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,  1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,  0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,  0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,  0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,  0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,  0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,  0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,  0, 1, 1, 0, 0, 0, 0, 1, 0, 0, 0],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,  0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0,  0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    ])
    observable_z = np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,  0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1])
    observable_x = np.array([0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1,  0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
    return StabilizerCodeUtilities(
        symplectic_matrix=symplectic_matrix,
        generator_anticommutators=anticommutators,
        z_observable=observable_z,
        x_observable=observable_x
    )
