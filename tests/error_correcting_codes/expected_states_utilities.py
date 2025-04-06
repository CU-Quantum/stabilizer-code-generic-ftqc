from abc import ABC, abstractmethod

from stim_experiments.utilities import DENSITY_MATRIX_TYPE


class ExpectedStatesUtilities(ABC):
    @abstractmethod
    def get_logical_zero_density_matrix(self) -> DENSITY_MATRIX_TYPE:
        pass

    @abstractmethod
    def get_logical_one_density_matrix(self) -> DENSITY_MATRIX_TYPE:
        pass
