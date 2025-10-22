from itertools import combinations

import numpy as np
from numpy._typing import NDArray
from pymatching import Matching
from scipy.sparse import csc_matrix
from sinter import CompiledDecoder


class CompiledDecoderByMatrix(CompiledDecoder):
    def __init__(self,
                 symplectic_matrix: NDArray[NDArray[int]],
                 syndrome_to_noise: dict[tuple, NDArray[int]],
                 distance: int,
                 observables: NDArray[NDArray[int]]):
        super().__init__()
        self._symplectic_matrix = symplectic_matrix
        self._syndrome_to_noise = syndrome_to_noise
        self._distance = distance
        self._observables = observables

    def decode_shots_bit_packed(self, *, bit_packed_detection_event_data: np.ndarray) -> np.ndarray:
        unpacked = np.unpackbits(bit_packed_detection_event_data, axis=1, bitorder='little')[:, :self._symplectic_matrix.shape[0]]
        predictions = np.zeros((unpacked.shape[0], len(self._observables)), dtype=np.uint8)
        if unpacked.max():
            for i, syndrome in enumerate(unpacked):
                noise = self._syndrome_to_noise.get(tuple(syndrome))
                if noise is not None:
                    predictions[i] = (self._observables @ noise) % 2
        return np.packbits(predictions, axis=1, bitorder='little')
