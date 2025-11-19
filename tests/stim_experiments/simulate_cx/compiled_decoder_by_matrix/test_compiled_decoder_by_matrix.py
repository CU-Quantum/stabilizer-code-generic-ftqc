import pickle
from pathlib import Path

import numpy as np

from stim_experiments.simulate_cx.decoder_by_matrix.compiled_decoder_by_matrix import CompiledDecoderByMatrix


class TestCompiledDecoderByMatrix:
    def test_spot(self):
        script_dir = Path(__file__).parent
        with open(Path(script_dir, "five_qubit_decoder_lookup_table.pickle"), "rb") as f:
            lookup_table = pickle.load(f)
        with open(Path(script_dir, "five_qubit_combined_symplectic_observable.pickle"), "rb") as f:
            observable = pickle.load(f)
        bit_packed_error = np.array([[11, 0, 44, 0, 176, 0, 0]], dtype=np.uint8)
        predicted_observable = CompiledDecoderByMatrix(
            syndrome_to_noise=lookup_table,
            distance=3,
            observables=observable
        ).decode_shots_bit_packed(bit_packed_detection_event_data=bit_packed_error)
        actual_observable = [1]
        assert np.allclose(predicted_observable, actual_observable)
