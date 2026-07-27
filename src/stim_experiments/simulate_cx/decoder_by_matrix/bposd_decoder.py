import numpy as np
from ldpc.bposd_decoder import BpOsdDecoder
from ldpc.ckt_noise import detector_error_model_to_check_matrices
from sinter import CompiledDecoder, Decoder
from stim import DetectorErrorModel


class BpOsdDecoderForSinter(Decoder):
    def __init__(self,
                 max_iter: int = 100,
                 bp_method: str = 'ms',
                 ms_scaling_factor: float = 0.625,
                 schedule: str = 'parallel',
                 osd_method: str = 'osd_cs',
                 osd_order: int = 10):
        self._max_iter = max_iter
        self._bp_method = bp_method
        self._ms_scaling_factor = ms_scaling_factor
        self._schedule = schedule
        self._osd_method = osd_method
        self._osd_order = osd_order

    def compile_decoder_for_dem(self, *, dem: DetectorErrorModel) -> CompiledDecoder:
        matrices = detector_error_model_to_check_matrices(dem, allow_undecomposed_hyperedges=True)
        bposd = BpOsdDecoder(
            matrices.check_matrix,
            error_channel=list(matrices.priors),
            max_iter=self._max_iter,
            bp_method=self._bp_method,
            ms_scaling_factor=self._ms_scaling_factor,
            schedule=self._schedule,
            osd_method=self._osd_method,
            osd_order=self._osd_order,
        )
        return CompiledBpOsdDecoder(bposd=bposd,
                                    observables_matrix=matrices.observables_matrix,
                                    num_detectors=dem.num_detectors)


class CompiledBpOsdDecoder(CompiledDecoder):
    def __init__(self, bposd: BpOsdDecoder, observables_matrix, num_detectors: int):
        self._bposd = bposd
        self._observables_matrix = observables_matrix
        self._num_detectors = num_detectors
        self._num_observables = observables_matrix.shape[0]
        self._syndrome_cache = {np.zeros(num_detectors, dtype=np.uint8).tobytes(): np.zeros(self._num_observables, dtype=np.uint8)}

    def decode_shots_bit_packed(self, *, bit_packed_detection_event_data: np.ndarray) -> np.ndarray:
        unpacked = np.unpackbits(bit_packed_detection_event_data, axis=1, bitorder='little')[:, :self._num_detectors]
        predictions = np.zeros((unpacked.shape[0], self._num_observables), dtype=np.uint8)
        for i, syndrome in enumerate(unpacked):
            key = syndrome.tobytes()
            prediction = self._syndrome_cache.get(key)
            if prediction is None:
                correction = self._bposd.decode(syndrome)
                prediction = ((self._observables_matrix @ correction) % 2).astype(np.uint8)
                if len(self._syndrome_cache) < 10_000_000:
                    self._syndrome_cache[key] = prediction
            predictions[i] = prediction
        return np.packbits(predictions, axis=1, bitorder='little')
