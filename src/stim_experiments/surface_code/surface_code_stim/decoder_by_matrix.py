from numpy._typing import NDArray
from pymatching import Matching
from scipy.sparse import csc_matrix
from sinter import CompiledDecoder, Decoder
from stim import DetectorErrorModel

from stim_experiments.surface.gsch import CompiledDecoderMatrix


class DecoderByMatrix(Decoder):
    def __init__(self, symplectic_matrix: NDArray[NDArray[int]]):
        self._symplectic_matrix = symplectic_matrix

    def compile_decoder_for_dem(
            self,
            *,
            dem: DetectorErrorModel,
    ) -> CompiledDecoder:
        H = self._symplectic_matrix
        matching = Matching.from_check_matrix(H)
        return CompiledDecoderMatrix(matching=matching)
