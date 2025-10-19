import numpy as np
from pymatching import Matching
from scipy.sparse import csc_matrix
from sinter import CompiledDecoder, Decoder
from stim._stim_polyfill import DetectorErrorModel

from stim_experiments.surface.gsch import CompiledDecoderMatrix


class DecoderByMatrix(Decoder):
    def __init__(self, symplectic_matrix: list[list[bool]]):
        self._symplectic_matrix = symplectic_matrix

    def compile_decoder_for_dem(
            self,
            *,
            dem: DetectorErrorModel,
    ) -> CompiledDecoder:
        H = csc_matrix(self._symplectic_matrix)
        observables = csc_matrix([[1, 0, 0, 0, 0]])
        error_probability = 0.1
        weights = np.ones(H.shape[1]) * np.log((1 - error_probability) / error_probability)
        matching = Matching.from_check_matrix(H, weights=weights)
        return CompiledDecoderMatrix(matching=matching)
