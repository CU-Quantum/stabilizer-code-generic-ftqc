from typing import List

import numpy
from numpy._typing import NDArray


def partial_trace(rho: NDArray[NDArray[complex]], keep_qubits: List[int]) -> NDArray[NDArray[complex]]:
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
