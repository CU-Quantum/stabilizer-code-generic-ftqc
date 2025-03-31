from typing import List

import numpy
from cirq import KET_ONE, KET_ZERO, density_matrix_from_state_vector, kron
from numpy._typing import NDArray

DENSITY_MATRIX_TYPE = NDArray[NDArray[complex]]

KET_ZERO_DENSITY_MATRIX = density_matrix_from_state_vector(KET_ZERO.state_vector())
KET_ONE_DENSITY_MATRIX = density_matrix_from_state_vector(KET_ONE.state_vector())


def partial_trace(rho: DENSITY_MATRIX_TYPE, keep_qubits: List[int]) -> DENSITY_MATRIX_TYPE:
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

    reduced_dim = 2 ** len(keep_qubits)
    return reshaped_rho.reshape((reduced_dim, reduced_dim))
