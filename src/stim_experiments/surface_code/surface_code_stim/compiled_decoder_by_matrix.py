import numpy as np
from pymatching import Matching
from sinter import CompiledDecoder


class CompiledDecoderByMatrix(CompiledDecoder):
    def __init__(self, matching: Matching):
        super().__init__()
        self._matching = matching

    def decode_shots_bit_packed(self, *, bit_packed_detection_event_data: np.ndarray) -> np.ndarray:
        unpacked = np.unpackbits(bit_packed_detection_event_data, axis=1, bitorder='little')
        return self._matching.decode_batch(unpacked)
