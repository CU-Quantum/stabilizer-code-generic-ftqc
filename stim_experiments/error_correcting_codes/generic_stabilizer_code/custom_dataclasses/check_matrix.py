from dataclasses import dataclass, field
from typing import List, Tuple

from numpy._typing import NDArray
from numpy.linalg import matrix_rank

TYPE_CHECK_MATRIX = NDArray[NDArray[bool]]


@dataclass
class CheckMatrix:
    matrix: TYPE_CHECK_MATRIX
    qubit_order: List[int] = field(default_factory=list)

    def __post_init__(self):
        default_qubit_order = list(range(self.num_physical_qubits))
        self.qubit_order = self.qubit_order or default_qubit_order

        if sorted(self.qubit_order) != default_qubit_order:
            raise ValueError(f"Qubit order must be a permutation of the number of qubits. Order {self.qubit_order} was provided.")
        if self.matrix.shape[1] % 2:
            raise ValueError(f"Check matrix must have have an even number of columns. Shape {self.matrix.shape} was provided.")
        if self.num_logical_qubits < 0:
            raise ValueError(f"The number of rows must be less than half the number of columns. Shape {self.matrix.shape} was provided.")

    @property
    def num_logical_qubits(self) -> int:
        return self.num_physical_qubits - self.matrix.shape[0]

    @property
    def num_physical_qubits(self) -> int:
        return self.matrix.shape[1] // 2

    @property
    def rank_of_pauli_x_portion(self) -> int:
        pauli_x_portion = self.matrix[:, :self.num_physical_qubits]
        return matrix_rank(pauli_x_portion) if pauli_x_portion.nbytes else 0

    def swap_qubits(self, column_indices: Tuple[int, int]) -> None:
        self._swap_qubit_order(column_indices=column_indices)
        self._swap_columns(column_indices=column_indices)

    def _swap_qubit_order(self, column_indices: Tuple[int, int]) -> None:
        qubit_indices = tuple(column_index % self.num_physical_qubits for column_index in column_indices)
        tmp = self.qubit_order[qubit_indices[0]]
        self.qubit_order[qubit_indices[0]] = qubit_indices[1]
        self.qubit_order[qubit_indices[1]] = tmp

    def _swap_columns(self, column_indices: Tuple[int, int]) -> None:
        respective_pauli_indices = tuple((index + self.num_physical_qubits) % self.matrix.shape[1] for index in column_indices)
        for indices in (column_indices, respective_pauli_indices):
            self.matrix[:, indices] = self.matrix[:, list(reversed(indices))]

    def add_rows(self, row_index: int, target_row_index: int) -> None:
        self.matrix[target_row_index] += self.matrix[row_index]
        self.matrix[target_row_index] %= 2
