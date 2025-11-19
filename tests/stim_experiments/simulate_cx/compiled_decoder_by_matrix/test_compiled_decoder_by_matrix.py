import pickle
from pathlib import Path

import numpy as np

from stim_experiments.simulate_cx.decoder_by_matrix.decoder_by_matrix import DecoderByMatrix


class TestCompiledDecoderByMatrix:
    def test_spot(self):
        script_dir = Path(__file__).parent
        with open(Path(__file__).parent / 'five_qubit_combined_symplectic_matrix.pickle', "rb") as f:
            self._five_qubit_symplectic_matrix = pickle.load(f)
        with open(script_dir / 'five_qubit_combined_symplectic_observable.pickle', 'rb') as f:
            observable = pickle.load(f)
        bit_packed_error = np.array([[11, 0, 44, 0, 176, 0, 0]], dtype=np.uint8)

        compiled_decoder = DecoderByMatrix(
            symplectic_matrix=self._five_qubit_symplectic_matrix,
            distance=3,
            observables=observable,
            modified_index=17,
            num_target_data_qubits=5
        ).compile_decoder_for_dem(dem=None)
        predicted_observable = compiled_decoder.decode_shots_bit_packed(bit_packed_detection_event_data=bit_packed_error)
        actual_observable = [1]
        assert np.allclose(predicted_observable, actual_observable)
        # syndrome = [True, True, False, True, False, False, False, False, False, False, False, False, False, False, False, False, False, False]
        # wrong_noise =    [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        # expected_noise = [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        # TODO: it looks like the prediction is correct. Fix circuit observables. Also perhaps do multiple observables.
