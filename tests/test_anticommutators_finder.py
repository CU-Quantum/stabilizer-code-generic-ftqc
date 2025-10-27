import numpy as np

from anticommutators_finder import anticommutators_for_generators
from predefined_check_matrix_values import (
    get_check_matrix_values_dodecacode,
    get_check_matrix_values_5_qubit,
)


def _verify(G: np.ndarray, A: np.ndarray) -> None:
    G = (G % 2).astype(np.uint8)
    A = (A % 2).astype(np.uint8)
    assert G.shape[0] == A.shape[0]
    assert G.shape[1] == A.shape[1]
    prod = (G @ A.T) % 2
    I = np.eye(G.shape[0], dtype=np.uint8)
    assert np.array_equal(prod, I), f"G @ A.T mod 2 != I; got\n{prod}\n"


def test_anticommutators_dodecacode():
    G = get_check_matrix_values_dodecacode().astype(np.uint8)
    A = anticommutators_for_generators(G)
    _verify(G, A)


def test_anticommutators_five_qubit():
    G = get_check_matrix_values_5_qubit().astype(np.uint8)
    A = anticommutators_for_generators(G)
    _verify(G, A)
