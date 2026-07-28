from collections import defaultdict

import numpy as np
from sinter import CompiledDecoder, Decoder
from stim import DetectorErrorModel

from ldpc.ckt_noise import detector_error_model_to_check_matrices

from stim_experiments.simulate_cx.decoder_by_matrix.bposd_decoder import BpOsdDecoderForSinter


class ExactMwDemDecoder(Decoder):
    def __init__(self, fallback_decoder: Decoder = None):
        self._fallback_decoder = fallback_decoder

    def compile_decoder_for_dem(self, *, dem: DetectorErrorModel) -> CompiledDecoder:
        matrices = detector_error_model_to_check_matrices(dem, allow_undecomposed_hyperedges=True)
        check_matrix = matrices.check_matrix.toarray().astype(bool)
        observables_matrix = matrices.observables_matrix.toarray().astype(np.uint8)
        priors = np.array(matrices.priors)
        fallback = (self._fallback_decoder or BpOsdDecoderForSinter()).compile_decoder_for_dem(dem=dem)
        return CompiledExactMwDemDecoder(check_matrix=check_matrix,
                                         observables_matrix=observables_matrix,
                                         priors=priors,
                                         fallback=fallback)


class CompiledExactMwDemDecoder(CompiledDecoder):
    def __init__(self, check_matrix, observables_matrix, priors, fallback: CompiledDecoder):
        self._check_matrix = check_matrix
        self._observables_matrix = observables_matrix
        self._priors = priors
        self._fallback = fallback
        self._num_detectors, self._num_mechanisms = check_matrix.shape
        self._num_observables = observables_matrix.shape[0]
        self._columns = check_matrix.T
        self._observable_columns = observables_matrix.T
        self._low_weight_table = self._build_low_weight_table()
        self._prediction_cache = {}

    def _build_low_weight_table(self):
        table = defaultdict(lambda: defaultdict(float))
        num_mechanisms = self._num_mechanisms
        log_priors = np.log(self._priors)
        for i in range(num_mechanisms):
            key = (1, self._columns[i].tobytes())
            table[key][tuple(self._observable_columns[i])] += np.exp(log_priors[i])
        for i in range(num_mechanisms):
            pair_syndromes = self._columns[i + 1:] ^ self._columns[i]
            pair_observables = self._observable_columns[i + 1:] ^ self._observable_columns[i]
            pair_log_priors = log_priors[i + 1:] + log_priors[i]
            for j in range(pair_syndromes.shape[0]):
                key = (2, pair_syndromes[j].tobytes())
                table[key][tuple(pair_observables[j])] += np.exp(pair_log_priors[j])
        return {key: dict(value) for key, value in table.items()}

    def decode_shots_bit_packed(self, *, bit_packed_detection_event_data: np.ndarray) -> np.ndarray:
        unpacked = np.unpackbits(bit_packed_detection_event_data, axis=1, bitorder='little')[:, :self._num_detectors].astype(bool)
        predictions = np.zeros((unpacked.shape[0], self._num_observables), dtype=np.uint8)
        for i, syndrome in enumerate(unpacked):
            predictions[i] = self._decode_single(syndrome)
        return np.packbits(predictions, axis=1, bitorder='little')

    def _decode_single(self, syndrome) -> np.ndarray:
        if not syndrome.any():
            return np.zeros(self._num_observables, dtype=np.uint8)
        key = syndrome.tobytes()
        prediction = self._prediction_cache.get(key)
        if prediction is None:
            prediction = self._decode_by_weight(syndrome, key)
            if len(self._prediction_cache) < 10_000_000:
                self._prediction_cache[key] = prediction
        return prediction

    def _decode_by_weight(self, syndrome, key) -> np.ndarray:
        for weight in (1, 2):
            observable_classes = self._low_weight_table.get((weight, key))
            if observable_classes:
                return np.array(max(observable_classes, key=observable_classes.get), dtype=np.uint8)
        observable_classes = defaultdict(float)
        for m in range(self._num_mechanisms):
            residual_key = (2, (syndrome ^ self._columns[m]).tobytes())
            for observable, probability in self._low_weight_table.get(residual_key, {}).items():
                combined = tuple(np.array(observable, dtype=np.uint8) ^ self._observable_columns[m])
                observable_classes[combined] += probability * self._priors[m]
        if observable_classes:
            return np.array(max(observable_classes, key=observable_classes.get), dtype=np.uint8)
        packed = np.packbits(syndrome.astype(np.uint8)[None, :], axis=1, bitorder='little')
        prediction = self._fallback.decode_shots_bit_packed(bit_packed_detection_event_data=packed)
        return np.unpackbits(prediction, axis=1, bitorder='little')[0, :self._num_observables]
