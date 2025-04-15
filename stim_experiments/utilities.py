from typing import List, Union

import numpy
from cirq import KET_ONE, KET_ZERO, density_matrix_from_state_vector
from numpy._typing import NDArray

TYPE_STATE_VECTOR = NDArray[complex]
TYPE_DENSITY_MATRIX = NDArray[NDArray[complex]]
TYPE_STATE_VECTOR_OR_DENSITY_MATRIX = Union[TYPE_DENSITY_MATRIX, TYPE_STATE_VECTOR]

KET_ZERO_STATE_VECTOR = KET_ZERO.state_vector()
KET_ONE_STATE_VECTOR = KET_ONE.state_vector()
KET_ZERO_DENSITY_MATRIX = density_matrix_from_state_vector(KET_ZERO.state_vector())
KET_ONE_DENSITY_MATRIX = density_matrix_from_state_vector(KET_ONE.state_vector())
KET_PLUS_DENSITY_MATRIX = density_matrix_from_state_vector((1 / numpy.sqrt(2)) * (KET_ZERO.state_vector() + KET_ONE.state_vector()))


def partial_trace(rho: TYPE_DENSITY_MATRIX, keep_qubits: List[int]) -> TYPE_DENSITY_MATRIX:
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
    dim = int(numpy.log2(rho.shape[0]))
    if any(q >= dim or q < 0 for q in keep_qubits):
        raise ValueError("Qubit index out of range.")

    trace_out = [q for q in range(dim) if q not in keep_qubits]
    reshaped_rho = rho.reshape([2] * (2 * dim))

    for qubit in reversed(trace_out):
        reshaped_rho = numpy.trace(reshaped_rho, axis1=qubit, axis2=qubit + dim)
        dim -= 1

    reduced_dim = 2 ** dim
    return reshaped_rho.reshape((reduced_dim, reduced_dim))


def int_to_binary_array(num: int, num_elements: int) -> List[int]:
    return list(map(int, bin(num)[2:].rjust(num_elements, '0')))


def binary_array_to_int(binary_array: List[int]) -> int:
    return int(''.join(map(str, binary_array)), 2)
