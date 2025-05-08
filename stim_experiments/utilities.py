from contextlib import contextmanager
from typing import ContextManager, Generator, Optional

from cirq import KET_ONE, KET_PLUS, KET_ZERO, LineQubit, density_matrix_from_state_vector, kron
from numpy import array, log2, sqrt, trace
from numpy._typing import NDArray

TYPE_STATE_VECTOR = NDArray[complex]
TYPE_DENSITY_MATRIX = NDArray[NDArray[complex]]
TYPE_STATE_VECTOR_OR_DENSITY_MATRIX = TYPE_DENSITY_MATRIX | TYPE_STATE_VECTOR

KET_ZERO_STATE_VECTOR = KET_ZERO.state_vector()
KET_ONE_STATE_VECTOR = KET_ONE.state_vector()
KET_PLUS_STATE_VECTOR = KET_PLUS.state_vector()

KET_ZERO_DENSITY_MATRIX = density_matrix_from_state_vector(KET_ZERO.state_vector())
KET_ONE_DENSITY_MATRIX = density_matrix_from_state_vector(KET_ONE.state_vector())
KET_PLUS_DENSITY_MATRIX = density_matrix_from_state_vector(KET_PLUS_STATE_VECTOR)

def get_ket_cat_state_vector(num_qubits: int) -> TYPE_STATE_VECTOR:
    return (1/sqrt(2)) * (tensor(*[KET_ZERO_STATE_VECTOR] * num_qubits) + tensor(*[KET_ONE_STATE_VECTOR] * num_qubits))


def get_num_qubits_in_state(state: TYPE_STATE_VECTOR_OR_DENSITY_MATRIX) -> int:
    return int(log2(state.shape[0]))


def is_state_vector(state: TYPE_STATE_VECTOR_OR_DENSITY_MATRIX) -> bool:
    return len(state.shape) == 1


def partial_trace(rho: TYPE_DENSITY_MATRIX, keep_qubits: list[int]) -> TYPE_DENSITY_MATRIX:
    """
    Compute the partial trace of a density matrix rho, keeping only the specified qubits.

    Parameters:
    rho : np.ndarray
        The density matrix (square matrix of size 2^n x 2^n).
    keep_qubits : list of int
        The qubits to keep (0-indexed).

    Returns:
    np.ndarray
        The reduced density matrix after tracing out the unspecified qubits.
    """
    dim = get_num_qubits_in_state(state=rho)
    if any(q >= dim or q < 0 for q in keep_qubits):
        raise ValueError("Qubit index out of range.")

    trace_out = [q for q in range(dim) if q not in keep_qubits]
    reshaped_rho = rho.reshape([2] * (2 * dim))

    for qubit in reversed(trace_out):
        reshaped_rho = trace(reshaped_rho, axis1=qubit, axis2=qubit + dim)
        dim -= 1

    reduced_dim = 2 ** dim
    return reshaped_rho.reshape((reduced_dim, reduced_dim))

def trace_out_ancillas_in_zero_state(state: TYPE_STATE_VECTOR_OR_DENSITY_MATRIX, num_ancillas: int) -> TYPE_STATE_VECTOR_OR_DENSITY_MATRIX:
        num_qubits = get_num_qubits_in_state(state=state)
        if is_state_vector(state=state):
            keep_indices = [not i % (2 ** num_ancillas) for i in range(len(state))]
            return state[keep_indices]
        else:
            return partial_trace(rho=state, keep_qubits=list(range(num_qubits)))


def int_to_binary_array(num: int, num_elements: int) -> list[int]:
    return list(map(int, bin(num)[2:].rjust(num_elements, '0')))


def binary_array_to_int(binary_array: list[int]) -> int:
    return int(''.join(map(str, binary_array)), 2)

def tensor(*states: TYPE_STATE_VECTOR_OR_DENSITY_MATRIX) -> TYPE_STATE_VECTOR_OR_DENSITY_MATRIX:
    return kron(*states, shape_len=len(states[0].shape)) if states else array([])


class FreshAncillasPool:
    # TODO test class

    _pool: list[LineQubit] = []
    _next_ancilla_num = 0

    def __new__(cls, first_ancilla_num: Optional[int] = None):
        cls._next_ancilla_num = cls._next_ancilla_num or first_ancilla_num or 0
        return cls(first_ancilla_num=first_ancilla_num)

    @contextmanager
    def _use_fresh_ancillas(self, num_ancillas: int) -> Generator[list[LineQubit], None, None]:
        if self._pool:
            ancillas = [self._pool.pop(0) for _ in range(num_ancillas)]
        else:
            ancillas = LineQubit.range(self._next_ancilla_num, num_ancillas)
            self._next_ancilla_num += num_ancillas

        yield ancillas

        for ancillas in ancillas:
            self._pool.append(ancillas)
