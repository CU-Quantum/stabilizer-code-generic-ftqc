from networkx.algorithms.threshold import eigenvectors
from numpy._typing import NDArray
from numpy.linalg import eig

from stim_experiments.utilities import TYPE_DENSITY_MATRIX


def get_pure_state_from_density_matrix_of_only_pure_states(density_matrix: TYPE_DENSITY_MATRIX) -> NDArray[complex]:
    eigenvalues, eigenvectors = eig(density_matrix)
    return eigenvalues

