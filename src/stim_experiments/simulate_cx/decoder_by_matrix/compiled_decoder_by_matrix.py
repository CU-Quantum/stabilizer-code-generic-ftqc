import numpy as np
from numpy._typing import NDArray
from sinter import CompiledDecoder


class CompiledDecoderByMatrix(CompiledDecoder):
    def __init__(self,
                 syndrome_to_noise: dict[tuple, NDArray[int]],
                 distance: int,
                 observables: NDArray[NDArray[int]],
                 final_detector_generator_indices: list[int] = None):
        super().__init__()
        self._syndrome_to_noise = syndrome_to_noise
        self._distance = distance
        self._observables = observables
        self._final_detector_generator_indices = final_detector_generator_indices or []

    def decode_shots_bit_packed(self, *, bit_packed_detection_event_data: np.ndarray) -> np.ndarray:
        unpacked = np.unpackbits(bit_packed_detection_event_data, axis=1, bitorder='little')
        syndromes = self.get_majority_vote(unpacked)
        predictions = np.zeros((unpacked.shape[0], len(self._observables)), dtype=np.uint8)
        if syndromes.max():
            for i, syndrome in enumerate(syndromes):
                noise = self._syndrome_to_noise.get(tuple(syndrome))
                if noise is not None:
                    predictions[i] = (self._observables @ noise) % 2
        return np.packbits(predictions, axis=1, bitorder='little')

    def get_majority_vote(self, unpacked_detection_event_data: np.ndarray):
        num_syndrome_bits = len(list(self._syndrome_to_noise.keys())[0])
        num_repeats = self._distance + 1
        differences = unpacked_detection_event_data[:, :num_syndrome_bits * num_repeats]
        differences = differences.reshape(differences.shape[0], num_repeats, num_syndrome_bits)
        rounds = (np.cumsum(differences, axis=1) % 2).astype(np.uint8)
        votes = rounds.sum(axis=1).astype(np.int64)
        num_votes = np.full(num_syndrome_bits, num_repeats)
        if self._final_detector_generator_indices:
            indices = np.array(self._final_detector_generator_indices)
            final_detectors = unpacked_detection_event_data[:, num_syndrome_bits * num_repeats:num_syndrome_bits * num_repeats + len(indices)]
            data_derived_syndromes = final_detectors ^ rounds[:, -1, indices]
            votes[:, indices] += data_derived_syndromes
            num_votes[indices] += 1
        return votes > num_votes // 2
