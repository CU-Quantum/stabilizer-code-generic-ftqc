from abc import ABC, abstractmethod

from stim_experiments.utilities import TYPE_DENSITY_MATRIX


class ExpectedStatesUtilities(ABC):
    @abstractmethod
    def get_logical_zero_density_matrix(self) -> TYPE_DENSITY_MATRIX:
        pass

    @abstractmethod
    def get_logical_one_density_matrix(self) -> TYPE_DENSITY_MATRIX:
        pass
