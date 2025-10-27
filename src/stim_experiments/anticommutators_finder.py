import numpy as np
from numpy._typing import NDArray

__all__ = [
    "anticommutators_for_generators",
]


def _gf2_rref_with_pivots(M: np.ndarray):
    """
    Row-reduce M over GF(2) and return (R, pivots).
    - R is the row-reduced form.
    - pivots is a list of pivot column indices.
    """
    M = (M.copy() % 2).astype(np.uint8)
    m, n = M.shape
    r = 0
    pivots: list[int] = []
    for c in range(n):
        pivot = None
        for i in range(r, m):
            if M[i, c]:
                pivot = i
                break
        if pivot is None:
            continue
        if pivot != r:
            M[[r, pivot]] = M[[pivot, r]]
        pivots.append(c)
        for i in range(m):
            if i != r and M[i, c]:
                M[i] ^= M[r]
        r += 1
        if r == m:
            break
    return M, pivots


def _gf2_inv(A: np.ndarray) -> np.ndarray:
    """Invert a square GF(2) matrix. Raises ValueError if singular."""
    A = (A.copy() % 2).astype(np.uint8)
    n = A.shape[0]
    I = np.eye(n, dtype=np.uint8)
    Aug = np.concatenate([A, I], axis=1)
    r = 0
    for c in range(n):
        piv = None
        for i in range(r, n):
            if Aug[i, c]:
                piv = i
                break
        if piv is None:
            raise ValueError("Matrix is singular over GF(2)")
        if piv != r:
            Aug[[r, piv]] = Aug[[piv, r]]
        for i in range(n):
            if i != r and Aug[i, c]:
                Aug[i] ^= Aug[r]
        r += 1
    return Aug[:, n:]


def anticommutators_for_generators(G: NDArray) -> NDArray:
    """
    Given generator matrix G (r x 2n) over GF(2), construct A (r x 2n) such that
    G @ A.T == I (mod 2). Uses invertible pivot submatrix.
    """
    G = (np.array(G) % 2).astype(np.uint8)
    r, _ = G.shape
    _, pivots = _gf2_rref_with_pivots(G)
    if len(pivots) != r:
        raise ValueError(f"Expected rank {r}, got {len(pivots)}; rows must be independent.")
    S = np.array(pivots, dtype=int)
    G_S = G[:, S]
    G_S_inv = _gf2_inv(G_S)
    A = np.zeros_like(G, dtype=np.uint8)
    A[:, S] = G_S_inv.T
    return A
