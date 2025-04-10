from dataclasses import dataclass

import numpy
from numpy.ma.core import allequal

from stim_experiments.error_correcting_codes.generic_stabilizer_code.custom_dataclasses.check_matrix import CheckMatrix


@dataclass
class CheckMatrixStandardized(CheckMatrix):
    def __post_init__(self):
        super().__post_init__()

        pauli_x_portion_identity = self.matrix[:self.rank_of_pauli_x_portion, :self.rank_of_pauli_x_portion]
        if not allequal(pauli_x_portion_identity, numpy.identity(self.rank_of_pauli_x_portion)):
            raise ValueError("The first (r)x(r) submatrix must be the identity.")

        pauli_x_portion_zeros = self.matrix[self.rank_of_pauli_x_portion:, :self.num_physical_qubits]
        if any(pauli_x_portion_zeros.flatten()):
            raise ValueError("All rows in the pauli_x portion below the rank must be 0.")

        pauli_z_portion_zeros = self.matrix[:self.rank_of_pauli_x_portion, self.num_physical_qubits + self.rank_of_pauli_x_portion:-self.num_logical_qubits]
        if any(pauli_z_portion_zeros.flatten()):
            raise ValueError("The (r)x(n-k-r) submatrix beginning at index [0, n+r] must be 0.")

        pauli_z_portion_zeros = self.matrix[self.rank_of_pauli_x_portion:, self.num_physical_qubits + self.rank_of_pauli_x_portion:-self.num_logical_qubits]
        if not allequal(pauli_z_portion_zeros, numpy.identity(self.num_physical_qubits - self.num_logical_qubits - self.rank_of_pauli_x_portion)):
            raise ValueError("The (n-k-r)x(n-k-r) submatrix beginning at index [r, n+r] must be the identity.")

    @property
    def a1_submatrix(self) -> numpy.ndarray:
        return self.matrix[:self.rank_of_pauli_x_portion, self.rank_of_pauli_x_portion:self.num_physical_qubits - self.num_logical_qubits]

    @property
    def a2_submatrix(self) -> numpy.ndarray:
        return self.matrix[:self.rank_of_pauli_x_portion, self.num_physical_qubits - self.num_logical_qubits:self.num_physical_qubits]

    @property
    def b_submatrix(self) -> numpy.ndarray:
        return self.matrix[:self.rank_of_pauli_x_portion, self.num_physical_qubits:self.num_physical_qubits + self.rank_of_pauli_x_portion]

    @property
    def c_submatrix(self) -> numpy.ndarray:
        return self.matrix[:self.rank_of_pauli_x_portion, -self.num_logical_qubits:]

    @property
    def d_submatrix(self) -> numpy.ndarray:
        return self.matrix[self.rank_of_pauli_x_portion:, self.num_physical_qubits:self.num_physical_qubits + self.rank_of_pauli_x_portion]

    @property
    def e_submatrix(self) -> numpy.ndarray:
        return self.matrix[self.rank_of_pauli_x_portion:, -self.num_logical_qubits:]

    def __eq__(self, other):
        return self.matrix.tolist() == other.matrix.tolist() and self.qubit_order == other.qubit_order
