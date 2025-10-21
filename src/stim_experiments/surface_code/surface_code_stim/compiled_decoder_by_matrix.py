from itertools import combinations

import numpy as np
from numpy._typing import NDArray
from pymatching import Matching
from scipy.sparse import csc_matrix
from sinter import CompiledDecoder


class CompiledDecoderByMatrix(CompiledDecoder):
    def __init__(self, symplectic_matrix: NDArray[NDArray[int]], distance: int, observables: NDArray[NDArray[int]]):
        super().__init__()
        self._symplectic_matrix = symplectic_matrix
        self._distance = distance
        self._observables = observables

    def decode_shots_bit_packed(self, *, bit_packed_detection_event_data: np.ndarray) -> np.ndarray:
        # Matching.from_check_matrix(csc_matrix(self._symplectic_matrix))
        unpacked = np.unpackbits(bit_packed_detection_event_data, axis=1, bitorder='little')
        predictions = np.zeros((unpacked.shape[0], len(self._observables)), dtype=np.uint8)
        if not unpacked.max():
            return predictions

        possible_combos = [combo for i in range(1, (self._distance - 1) // 2 + 1) for combo in combinations(range(self._symplectic_matrix.shape[1]), i)]
        for combo in possible_combos:
            found_noise = np.zeros(self._symplectic_matrix.shape[1], dtype=np.uint8)
            found_noise[list(combo)] = np.ones(len(combo))
            found_syndrome = self._symplectic_matrix @ found_noise
            indices_matching = np.where(np.all(unpacked == found_syndrome, axis=1))[0]
            if len(indices_matching):
                noisy_shots = np.array([found_noise for _ in range(len(indices_matching))])
                predictions[indices_matching] = noisy_shots @ self._observables.T
        # for syndrome in unpacked:
        #     found_noise = np.zeros(self._symplectic_matrix.shape[0], dtype=np.uint8)
        #     if any(syndrome):
        #         for combo in possible_combos:
        #             found_noise[combo] = np.ones(len(combo))
        #             found_syndrome = self._symplectic_matrix @ found_noise
        #             if allequal(found_syndrome, syndrome):
        #                 break
        #     predictions.append(found_noise)
        return predictions
