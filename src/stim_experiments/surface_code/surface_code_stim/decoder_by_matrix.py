from numpy._typing import NDArray
from pymatching import Matching
from scipy.sparse import csc_matrix
from sinter import CompiledDecoder, Decoder
from stim import DetectorErrorModel

from stim_experiments.surface_code.surface_code_stim.compiled_decoder_by_matrix import CompiledDecoderByMatrix


class DecoderByMatrix(Decoder):
    def __init__(self, symplectic_matrix: NDArray[NDArray[int]], distance: int, observables: NDArray[int]):
        self._symplectic_matrix = symplectic_matrix
        self._distance = distance
        self._observables = observables

    def compile_decoder_for_dem(
            self,
            *,
            dem: DetectorErrorModel,
    ) -> CompiledDecoder:
        # H = csc_matrix(self._symplectic_matrix)
        # matching = Matching.from_check_matrix(H)
        return CompiledDecoderByMatrix(symplectic_matrix=self._symplectic_matrix, distance=self._distance, observables=self._observables)
