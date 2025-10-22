from itertools import combinations

import numpy as np
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
        possible_combos = [combo
                           for i in range(1, (self._distance - 1) // 2 + 1)
                           for combo in combinations(range(self._symplectic_matrix.shape[1]), i)]
        syndrome_to_noise = {
            tuple(syndrome): noise
            for combo in possible_combos
            for syndrome, noise in self._syndrome_and_noise(combo)
            if syndrome.max()
        }
        return CompiledDecoderByMatrix(
            symplectic_matrix=self._symplectic_matrix,
            syndrome_to_noise=syndrome_to_noise,
            distance=self._distance,
            observables=self._observables
        )

    def _syndrome_and_noise(self, combo):
        found_noise = np.zeros(self._symplectic_matrix.shape[1], dtype=np.uint8)
        found_noise[list(combo)] = np.ones(len(combo))
        found_syndrome = (self._symplectic_matrix @ found_noise) % 2
        return [(found_syndrome, found_noise)]
