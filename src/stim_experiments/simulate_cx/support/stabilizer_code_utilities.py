from collections import deque
from functools import cached_property

import numpy as np
from numpy._typing import NDArray
from stim import Circuit

from generalized_shor_code_generators import GeneralizedShorCodeGenerators
from predefined_check_matrix_values import get_check_matrix_values_5_qubit, get_check_matrix_values_17_1_7, \
    get_check_matrix_values_dodecacode, \
    get_check_matrix_values_golay, get_check_matrix_values_tetrahedral


class StabilizerCodeUtilities:
    def __init__(self,
                 symplectic_matrix: NDArray[NDArray[int]],
                 generator_anticommutators: NDArray[NDArray[int]],
                 z_observable: NDArray[int],
                 x_observable: NDArray[int],
                 target_code_utilities: 'StabilizerCodeUtilities' = None,
                 qubit_id_start: int = 0,
                 row_coord_start: int = 0,
                 existing_ancilla_indices: list[int] = None,
                 code_name: str = None,):
        self.symplectic_matrix = symplectic_matrix
        self.row_coord_start = row_coord_start
        self.z_observable = z_observable
        self.x_observable = x_observable
        self.existing_ancilla_indices = existing_ancilla_indices or []
        self.code_name = code_name

        self._generator_anticommutators = generator_anticommutators
        self._qubit_id_start = qubit_id_start
        self._target_code_utilities = target_code_utilities

    def get_init(self):
        return Circuit(f"""
            R {' '.join(map(str, self.data_indices))}
            R {' '.join(map(str, self.all_ancilla_qubits))}
        """)

    def get_encoding_by_stabilizer(self):
        return Circuit(f"""
            {self.get_stabilizers(is_encoding=True)}
            {self._encode_z_observable()}
        """)

    def _encode_z_observable(self):
        circuit = Circuit()
        self.measure_stabilizer_using_cat_state(self.z_observable, circuit)
        ancilla_index = self.stabilizer_ancilla
        self.apply_stabilizer(self.x_observable, circuit, [ancilla_index] * self.num_cat_appier_ancillas)
        circuit.append('R', [ancilla_index] + self.cat_applier_ancillas)
        return circuit

    def measure_stabilizer_using_cat_state(self, stabilizer, circuit):
        ancilla_index = self.stabilizer_ancilla
        self.prepare_cat_state(ancilla_index, circuit)
        self.apply_stabilizer(stabilizer, circuit, [ancilla_index] + self.cat_applier_ancillas)
        self.unprepare_cat_state(ancilla_index, circuit)
        circuit.append('M', ancilla_index)

    def get_stabilizers(self, modify_stabilizer: Circuit = None, modified_generator: int = None, is_encoding: bool = False, measurement_error_rate: float = None) -> Circuit:
        circuit = Circuit()
        ancilla_index = self.stabilizer_ancilla
        for generator_num, (stabilizer, anticommutator) in enumerate(zip(self.symplectic_matrix, self._generator_anticommutators)):
            self.prepare_cat_state(ancilla_index, circuit)
            self.apply_stabilizer(stabilizer, circuit, [ancilla_index] + self.cat_applier_ancillas)
            if modify_stabilizer and modified_generator == generator_num:
                circuit.append_from_stim_program_text(str(modify_stabilizer))
            self.unprepare_cat_state(ancilla_index, circuit)
            circuit.append('M', ancilla_index, measurement_error_rate)
            if is_encoding:
                self.apply_stabilizer(anticommutator, circuit, [ancilla_index] * self.num_cat_appier_ancillas)
            circuit.append('R', [ancilla_index] + self.cat_applier_ancillas)
        return circuit

    def prepare_cat_state(self, ancilla_index: int, circuit: Circuit):
        circuit.append('H', ancilla_index)
        for measurement_index in self.cat_applier_ancillas:
            circuit.append('CX', [ancilla_index, measurement_index])

    def unprepare_cat_state(self, ancilla_index: int, circuit: Circuit):
        for measurement_index in self.cat_applier_ancillas:
            circuit.append('CX', [ancilla_index, measurement_index])
        circuit.append('H', ancilla_index)

    def apply_stabilizer(self, stabilizer, circuit, ancillas):
        x_qubits = np.argwhere(stabilizer[:len(self.data_indices)] == 1).flatten()
        z_qubits = np.argwhere(stabilizer[len(self.data_indices):] == 1).flatten()
        if len(x_qubits):
            circuit.append('CX', list(j for i in zip(ancillas[:len(x_qubits)], np.array(self.data_indices)[x_qubits]) for j in i))
        if len(z_qubits):
            circuit.append('CZ', list(j for i in zip(ancillas[len(x_qubits):], np.array(self.data_indices)[z_qubits]) for j in i))

    @property
    def last_qubit_index(self):
        return self.all_ancilla_qubits[-1]

    @property
    def all_ancilla_qubits(self):
        return [self.stabilizer_ancilla] + self.cat_applier_ancillas

    @cached_property
    def cat_applier_ancillas(self):
        return [self.ancillas_pool.popleft() for _ in range(self.num_cat_appier_ancillas)]

    @cached_property
    def stabilizer_ancilla(self) -> int:
        return self.ancillas_pool.popleft()

    @cached_property
    def ancillas_pool(self) -> deque[int]:
        num_ancillas = 1
        start_ancilla_index = self.data_indices[-1] + 1
        return deque(self.existing_ancilla_indices + list(range(start_ancilla_index, start_ancilla_index + num_ancillas + self.num_cat_appier_ancillas + 1)))

    @property
    def num_cat_appier_ancillas(self):
        num_for_self = max(np.count_nonzero(self.z_observable),
                   np.count_nonzero(self.x_observable),
                   *np.count_nonzero(self.symplectic_matrix, axis=1),
                   *np.count_nonzero(self._generator_anticommutators, axis=1))
        num_for_target = np.count_nonzero(self._target_code_utilities.x_observable) if self._target_code_utilities else 0
        return num_for_self + num_for_target

    @property
    def data_indices(self) -> list[int]:
        num_data_qubits = self.symplectic_matrix.shape[1] // 2
        return list(range(self._qubit_id_start, self._qubit_id_start + num_data_qubits))


def get_shor_h_observable_z(distance: int, num_qubits_per_cat_state: int = None) -> NDArray:
    if num_qubits_per_cat_state is None:
        num_qubits_per_cat_state = distance
    num_data = distance * num_qubits_per_cat_state
    z_part = np.zeros(num_data, dtype=int)
    z_part[::num_qubits_per_cat_state] = 1
    return np.concatenate([np.zeros(num_data, dtype=int), z_part])


def get_shor_h_observable_x(distance: int, num_qubits_per_cat_state: int = None) -> NDArray:
    if num_qubits_per_cat_state is None:
        num_qubits_per_cat_state = distance
    num_data = distance * num_qubits_per_cat_state
    x_part = np.zeros(num_data, dtype=int)
    x_part[:num_qubits_per_cat_state] = 1
    return np.concatenate([x_part, np.zeros(num_data, dtype=int)])


def get_shor_code_utilities(num_cat_states: int,
                            num_qubits_per_cat_state: int,
                            z_observable: NDArray,
                            x_observable: NDArray,
                            target_code_utilities: StabilizerCodeUtilities = None,
                            qubit_id_start: int = 0,
                            row_coord_start: int = 0,
                            existing_ancilla_indices: list[int] = None
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
        target_code_utilities=target_code_utilities,
        qubit_id_start=qubit_id_start,
        row_coord_start=row_coord_start,
        existing_ancilla_indices=existing_ancilla_indices,
        code_name='shor',
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
        symplectic_matrix=symplectic_matrix,
        generator_anticommutators=anticommutators,
        z_observable=observable_z,
        x_observable=observable_x
    )


def get_golay_code_utilities(balanced: bool = True):
    symplectic_matrix = get_check_matrix_values_golay(balanced=balanced)
    n_qubits = symplectic_matrix.shape[1] // 2
    n_stabilizers = symplectic_matrix.shape[0]
    assert n_stabilizers == 22 and n_qubits == 23
    r = n_stabilizers // 2

    H = symplectic_matrix[:r, :n_qubits].astype(np.uint8)

    anticom_z_solutions = np.zeros((r, n_qubits), dtype=np.uint8)
    for target_col in range(r):
        aug = np.zeros((r, n_qubits + 1), dtype=np.uint8)
        aug[:, :n_qubits] = H.copy()
        aug[target_col, n_qubits] = 1
        col = 0
        for row in range(r):
            while col < n_qubits:
                pivot_found = False
                for i in range(row, r):
                    if aug[i, col]:
                        aug[[row, i]] = aug[[i, row]]
                        pivot_found = True
                        break
                if pivot_found:
                    break
                col += 1
            if col >= n_qubits:
                break
            for i in range(r):
                if i != row and aug[i, col]:
                    aug[i] ^= aug[row]
            col += 1
        a = np.zeros(n_qubits, dtype=np.uint8)
        for row in range(r):
            pivot_col = None
            for j in range(n_qubits):
                if aug[row, j]:
                    pivot_col = j
                    break
            if pivot_col is not None:
                a[pivot_col] = aug[row, n_qubits]
        anticom_z_solutions[target_col] = a

    anticommutators = np.zeros((n_stabilizers, 2 * n_qubits), dtype=int)
    anticommutators[:r, n_qubits:] = anticom_z_solutions
    anticommutators[r:, :n_qubits] = anticom_z_solutions

    observable_x = np.concatenate([np.ones(n_qubits, dtype=int), np.zeros(n_qubits, dtype=int)])
    observable_z = np.concatenate([np.zeros(n_qubits, dtype=int), np.ones(n_qubits, dtype=int)])
    return StabilizerCodeUtilities(
        symplectic_matrix=symplectic_matrix,
        generator_anticommutators=anticommutators,
        z_observable=observable_z,
        x_observable=observable_x,
        code_name='golay',
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
        x_observable=observable_x,
        code_name='five_qubit',
    )


def get_17_1_7_code_utilities():
    n_qubits = 17
    symplectic_matrix = get_check_matrix_values_17_1_7()
    # Anticommutators: symplectic dual of the stabilizer rows (each row
    # anticommutes with exactly the corresponding stabilizer and commutes
    # with all others), used to fix the +1 eigenspace during encoding.
    anticommutators = np.array([
        [0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [1, 1, 1, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [1, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [1, 0, 1, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [1, 1, 1, 1, 1, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [1, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [1, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    ])
    observable_x = np.concatenate([np.ones(n_qubits, dtype=int), np.zeros(n_qubits, dtype=int)])
    observable_z = np.concatenate([np.zeros(n_qubits, dtype=int), np.ones(n_qubits, dtype=int)])
    return StabilizerCodeUtilities(
        symplectic_matrix=symplectic_matrix,
        generator_anticommutators=anticommutators,
        z_observable=observable_z,
        x_observable=observable_x,
        code_name='17_1_7',
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
        x_observable=observable_x,
        code_name='dodecacode',
    )


def get_gscx_code_utilities(distance: int) -> StabilizerCodeUtilities:
    utils = get_shor_code_utilities(
        num_cat_states=distance,
        num_qubits_per_cat_state=distance,
        z_observable=get_shor_h_observable_z(distance),
        x_observable=get_shor_h_observable_x(distance),
    )
    utils.code_name = 'gscx'
    return utils


def _gf2_rank(matrix):
    matrix = matrix.astype(np.uint8).copy()
    rows, cols = matrix.shape
    rank = 0
    for col in range(cols):
        if rank >= rows:
            break
        pivot = None
        for i in range(rank, rows):
            if matrix[i, col]:
                pivot = i
                break
        if pivot is None:
            continue
        matrix[[rank, pivot]] = matrix[[pivot, rank]]
        for i in range(rows):
            if i != rank and matrix[i, col]:
                matrix[i] ^= matrix[rank]
        rank += 1
    return rank


def _gf2_nullspace(matrix):
    matrix = matrix.astype(np.uint8).copy()
    rows, cols = matrix.shape
    pivots = []
    rank = 0
    for col in range(cols):
        if rank >= rows:
            break
        pivot = None
        for i in range(rank, rows):
            if matrix[i, col]:
                pivot = i
                break
        if pivot is None:
            continue
        matrix[[rank, pivot]] = matrix[[pivot, rank]]
        for i in range(rows):
            if i != rank and matrix[i, col]:
                matrix[i] ^= matrix[rank]
        pivots.append(col)
        rank += 1
    pivot_cols = set(pivots)
    free = [c for c in range(cols) if c not in pivot_cols]
    basis = []
    for f in free:
        vec = np.zeros(cols, dtype=np.uint8)
        vec[f] = 1
        for ri, pc in enumerate(pivots):
            vec[pc] = matrix[ri, f]
        basis.append(vec)
    return np.array(basis, dtype=np.uint8) if basis else np.zeros((0, cols), dtype=np.uint8)


def _gf2_in_rowspace(vec, matrix):
    return _gf2_rank(np.vstack([matrix, vec])) == _gf2_rank(matrix)


def _gf2_independent_rows(matrix):
    independent = []
    rank = 0
    for row in matrix:
        candidate = np.array(independent + [row], dtype=np.uint8) if independent else row.reshape(1, -1)
        if _gf2_rank(candidate) > rank:
            independent.append(row)
            rank += 1
    return np.array(independent, dtype=np.uint8)


def _gf2_solve(matrix, rhs):
    augmented = np.concatenate([matrix.astype(np.uint8), rhs.astype(np.uint8).reshape(-1, 1)], axis=1)
    rows, cols = augmented.shape
    rank = 0
    for col in range(cols - 1):
        if rank >= rows:
            break
        pivot = None
        for i in range(rank, rows):
            if augmented[i, col]:
                pivot = i
                break
        if pivot is None:
            continue
        augmented[[rank, pivot]] = augmented[[pivot, rank]]
        for i in range(rows):
            if i != rank and augmented[i, col]:
                augmented[i] ^= augmented[rank]
        rank += 1
    for i in range(rank, rows):
        if augmented[i, -1] and not augmented[i, :cols - 1].any():
            return None
    solution = np.zeros(cols - 1, dtype=np.uint8)
    pivots = []
    r = 0
    for col in range(cols - 1):
        if r >= rows:
            break
        pivot = None
        for i in range(r, rows):
            if augmented[i, col]:
                pivot = i
                break
        if pivot is None:
            continue
        pivots.append((r, col))
        r += 1
    for (row, col) in pivots:
        solution[col] = augmented[row, -1]
    return solution


def _gf2_symplectic_dual(symplectic_matrix):
    n = symplectic_matrix.shape[1] // 2
    num_rows = symplectic_matrix.shape[0]
    sx = symplectic_matrix[:, :n]
    sz = symplectic_matrix[:, n:]
    commutation_matrix = np.concatenate([sz, sx], axis=1)
    dual = []
    for i in range(num_rows):
        rhs = np.zeros(num_rows, dtype=np.uint8)
        rhs[i] = 1
        dual.append(_gf2_solve(commutation_matrix, rhs))
    return np.array(dual, dtype=np.uint8)


def get_bb_code_90_8_10_utilities():
    """[[90,8,10]] bivariate-bicycle (BB) QLDPC code (arXiv:2308.07915).

    The code has 8 logical qubits; a single paired (Z, X) logical qubit is
    selected so it can be used as a single-logical-qubit target code in the CX
    framework.  The stabilizers are reduced to an independent set and the
    anticommutators are the symplectic dual of the stabilizer rows.
    """
    ell, m = 15, 3
    a1, a2, a3 = 9, 1, 2
    b1, b2, b3 = 0, 2, 7
    n2 = ell * m
    n = 2 * n2
    i_ell = np.identity(ell, dtype=np.uint8)
    i_m = np.identity(m, dtype=np.uint8)
    x_shift = {i: np.kron(np.roll(i_ell, i, axis=1), i_m).astype(np.uint8) for i in range(ell)}
    y_shift = {i: np.kron(i_ell, np.roll(i_m, i, axis=1)).astype(np.uint8) for i in range(m)}
    a_mat = (x_shift[a1] + y_shift[a2] + y_shift[a3]) % 2
    b_mat = (y_shift[b1] + x_shift[b2] + x_shift[b3]) % 2
    hx = np.concatenate([a_mat, b_mat], axis=1)
    hz = np.concatenate([b_mat.T, a_mat.T], axis=1)

    num_logicals = n - _gf2_rank(hx) - _gf2_rank(hz)
    z_logicals = []
    for vec in _gf2_nullspace(hx):
        if _gf2_in_rowspace(vec, hz):
            continue
        candidate = np.array(z_logicals + [vec], dtype=np.uint8) if z_logicals else vec.reshape(1, -1)
        if _gf2_rank(candidate) > (_gf2_rank(np.array(z_logicals, dtype=np.uint8)) if z_logicals else 0):
            z_logicals.append(vec)
        if len(z_logicals) == num_logicals:
            break
    x_logicals = []
    for vec in _gf2_nullspace(hz):
        if _gf2_in_rowspace(vec, hx):
            continue
        candidate = np.array(x_logicals + [vec], dtype=np.uint8) if x_logicals else vec.reshape(1, -1)
        if _gf2_rank(candidate) > (_gf2_rank(np.array(x_logicals, dtype=np.uint8)) if x_logicals else 0):
            x_logicals.append(vec)
        if len(x_logicals) == num_logicals:
            break
    z_logicals = np.array(z_logicals, dtype=np.uint8)
    x_logicals = np.array(x_logicals, dtype=np.uint8)

    z_obs = z_logicals[0]
    x_obs = next(xl for xl in x_logicals if int((z_obs & xl).sum()) % 2 == 1)

    hx_ind = _gf2_independent_rows(hx)
    hz_ind = _gf2_independent_rows(hz)
    symplectic_matrix = np.concatenate([
        np.concatenate([hx_ind, np.zeros((hx_ind.shape[0], n), dtype=np.uint8)], axis=1),
        np.concatenate([np.zeros((hz_ind.shape[0], n), dtype=np.uint8), hz_ind], axis=1),
    ], axis=0)
    anticommutators = _gf2_symplectic_dual(symplectic_matrix)

    observable_z = np.concatenate([np.zeros(n, dtype=int), z_obs]).astype(int)
    observable_x = np.concatenate([x_obs, np.zeros(n, dtype=int)]).astype(int)
    return StabilizerCodeUtilities(
        symplectic_matrix=symplectic_matrix,
        generator_anticommutators=anticommutators,
        z_observable=observable_z,
        x_observable=observable_x,
        code_name='bb_code',
    )
