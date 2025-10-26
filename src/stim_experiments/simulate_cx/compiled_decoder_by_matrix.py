import numpy as np
from numpy._typing import NDArray
from sinter import CompiledDecoder


class CompiledDecoderByMatrix(CompiledDecoder):
    def __init__(self,
                 syndrome_to_noise: dict[tuple, NDArray[int]],
                 distance: int,
                 observables: NDArray[NDArray[int]]):
        super().__init__()
        self._syndrome_to_noise = syndrome_to_noise
        self._distance = distance
        self._observables = observables

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
        num_repeats = unpacked_detection_event_data.shape[1] // num_syndrome_bits
        unpadded = unpacked_detection_event_data[:, :num_syndrome_bits * num_repeats]
        majority_vote = unpadded.reshape(unpadded.shape[0], num_repeats, num_syndrome_bits).sum(axis=1) > (num_repeats // 2)
        return majority_vote
