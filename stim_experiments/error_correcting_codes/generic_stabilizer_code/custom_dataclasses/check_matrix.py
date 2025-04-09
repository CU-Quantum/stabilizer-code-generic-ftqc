from dataclasses import dataclass

from numpy._typing import NDArray
from numpy.linalg import matrix_rank

TYPE_CHECK_MATRIX = NDArray[NDArray[bool]]


@dataclass
class CheckMatrix:
    matrix: TYPE_CHECK_MATRIX
    num_logical_qubits: int = 1

    def __post_init__(self):
        if self.matrix.shape[1] % 2:
            raise ValueError("Check matrix must have have an even number of columns.")
        if self.matrix.shape[0] != self.num_physical_qubits - self.num_logical_qubits:
            raise ValueError("Check matrix must have n-k rows.")

    @property
    def num_physical_qubits(self) -> int:
        return self.matrix.shape[1] // 2

    @property
    def rank_of_pauli_x_portion(self) -> int:
        pauli_x_portion = self.matrix[:, :self.num_physical_qubits]
        return matrix_rank(pauli_x_portion)
