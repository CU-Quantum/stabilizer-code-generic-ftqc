import numpy as np
from ldpc.bposd_decoder import BpOsdDecoder
from ldpc.ckt_noise import detector_error_model_to_check_matrices
from sinter import CompiledDecoder, Decoder


def _filter_rows_cols(cm, row_mask):
    rows = np.where(row_mask)[0]
    sub = cm[rows, :]
    nz = np.diff(sub.indptr) > 0
    col_map = list(np.where(nz)[0])
    return sub[:, col_map].tocsc(), col_map


class PartitionDecoder(Decoder):
    def __init__(self, combined_symplectic_matrix,
                 num_target_stabilizers,
                 distance, modified_index,
                 target_decoder='bposd'):
        self._S = combined_symplectic_matrix
        self._n_tgt_stabs = num_target_stabilizers
        self._distance = distance
        self._modified_index = modified_index
        self._target_decoder = target_decoder

    def compile_decoder_for_dem(self, *, dem):
        matrices = detector_error_model_to_check_matrices(dem, allow_undecomposed_hyperedges=True)
        cm = matrices.check_matrix.tocsc()
        obs = matrices.observables_matrix.toarray().astype(np.uint8)
        priors = list(matrices.priors)
        num_detectors = dem.num_detectors

        if cm.shape[1] == 0:
            return _EmptyDecoder(num_detectors, obs.shape[0])

        num_gens = self._S.shape[0]
        num_repeats = self._distance + 1
        num_target = self._n_tgt_stabs

        is_target = np.zeros(num_detectors, dtype=bool)
        for r in range(num_repeats):
            is_target[r * num_gens:(r * num_gens) + num_target] = True

        # --- Target BP-OSD ---
        tgt_cm, tgt_map = _filter_rows_cols(cm, is_target)
        tgt_priors = [priors[c] for c in tgt_map]
        tgt_obs = obs[:, tgt_map]

        tgt_bposd = BpOsdDecoder(
            tgt_cm, error_channel=tgt_priors,
            max_iter=100, bp_method='ms', ms_scaling_factor=0.625,
            schedule='parallel', osd_method='osd_cs', osd_order=10,
        )
        tgt_lookup = None
        if self._target_decoder == 'lookup':
            tgt_lookup = _build_lookup_table(tgt_cm, tgt_obs, self._distance)

        # --- Control BP-OSD ---
        ctrl_cm, ctrl_map = _filter_rows_cols(cm, ~is_target)
        ctrl_priors = [priors[c] for c in ctrl_map]
        ctrl_obs = obs[:, ctrl_map]

        ctrl_bposd = BpOsdDecoder(
            ctrl_cm, error_channel=ctrl_priors,
            max_iter=100, bp_method='ms', ms_scaling_factor=0.625,
            schedule='parallel', osd_method='osd_cs', osd_order=10,
        )

        modified_detector_index = None
        if self._modified_index is not None and self._modified_index < num_gens:
            modified_detector_index = (num_repeats - 1) * num_gens + self._modified_index

        return CompiledPartitionDecoder(
            tgt_bposd=tgt_bposd, tgt_obs=tgt_obs, tgt_lookup=tgt_lookup,
            tgt_map=tgt_map, ctrl_bposd=ctrl_bposd, ctrl_map=ctrl_map,
            full_cm=cm, full_obs=obs,
            num_detectors=num_detectors,
            is_target=is_target,
            modified_detector_index=modified_detector_index,
        )


def _build_lookup_table(cm, obs, distance, max_combos=1_000_000):
    from itertools import combinations
    t = (distance - 1) // 2
    c = cm.tocsc()
    n = c.shape[1]
    n_obs = 1 if obs.ndim == 1 else obs.shape[0]
    table = {bytes(c.shape[0]): (np.zeros(n_obs, dtype=np.uint8), [])}
    for w in range(1, t + 1):
        nc = 1
        for k in range(w): nc = nc * (n - k) // (k + 1)
        if nc > max_combos: break
        for combo in combinations(range(n), w):
            syn = np.zeros(c.shape[0], dtype=np.uint8)
            pred = np.zeros(n_obs, dtype=np.uint8)
            for j in combo:
                syn ^= c[:, j].toarray().flatten().astype(np.uint8)
                if obs.ndim == 1: pred ^= obs[j]
                else: pred ^= obs[:, j]
            key = syn.tobytes()
            if key not in table:
                table[key] = (pred.astype(np.uint8), list(combo))
    return table


class _EmptyDecoder(CompiledDecoder):
    def __init__(self, n_det, n_obs):
        self._nd = n_det; self._no = n_obs
    def decode_shots_bit_packed(self, *, bit_packed_detection_event_data):
        u = np.unpackbits(bit_packed_detection_event_data, axis=1, bitorder='little')
        return np.zeros((u.shape[0], (self._no + 7) // 8), dtype=np.uint8)


class CompiledPartitionDecoder(CompiledDecoder):
    def __init__(self, tgt_bposd, tgt_obs, tgt_lookup, tgt_map,
                 ctrl_bposd, ctrl_map, full_cm, full_obs,
                 num_detectors, is_target, modified_detector_index):
        self._tgt_bposd = tgt_bposd
        self._tgt_obs = tgt_obs
        self._tgt_lookup = tgt_lookup
        self._tgt_map = tgt_map
        self._ctrl_bposd = ctrl_bposd
        self._ctrl_map = ctrl_map
        self._full_cm = full_cm
        self._full_obs = full_obs
        self._num_detectors = num_detectors
        self._is_target = is_target
        self._modified_detector_index = modified_detector_index

    def decode_shots_bit_packed(self, *, bit_packed_detection_event_data):
        unpacked = np.unpackbits(bit_packed_detection_event_data, axis=1,
                                 bitorder='little')[:, :self._num_detectors]
        num_shots = unpacked.shape[0]
        predictions = np.zeros((num_shots, (self._full_obs.shape[0] + 7) // 8),
                               dtype=np.uint8)

        td = unpacked[:, self._is_target]
        cd_raw = unpacked[:, ~self._is_target]

        for i in range(num_shots):
            ts = td[i].astype(np.uint8)
            cs = cd_raw[i].copy().astype(np.uint8)

            if not ts.any() and not cs.any():
                continue

            # Step 1: decode target
            tgt_corr = self._decode_target(ts)

            # Step 2: if target correction flips X observable, flip
            # the specific modified stabilizer detector in the control syndrome
            if (tgt_corr is not None and
                    self._modified_detector_index is not None):
                tgt_full = np.zeros(self._full_cm.shape[1], dtype=np.uint8)
                for j, col in enumerate(self._tgt_map):
                    tgt_full[col] = tgt_corr[j]
                # Check if target correction implies an observable flip
                tgt_x_flip = (self._full_obs @ tgt_full) % 2
                if tgt_x_flip.any():
                    # The modified detector is in the control partition.
                    # Find its index within the control-only unpacked array.
                    mod_idx_in_ctrl = (
                        self._modified_detector_index
                        - np.sum(self._is_target[:self._modified_detector_index])
                    )
                    cs[mod_idx_in_ctrl] ^= 1

            # Step 3: decode control
            ctrl_corr = self._ctrl_bposd.decode(cs) if cs.any() else None

            # Step 4: union correction + observable
            full_c = np.zeros(self._full_cm.shape[1], dtype=np.uint8)
            if tgt_corr is not None:
                for j, col in enumerate(self._tgt_map):
                    full_c[col] |= tgt_corr[j]
            if ctrl_corr is not None:
                for j, col in enumerate(self._ctrl_map):
                    full_c[col] |= ctrl_corr[j]

            pred = ((self._full_obs @ full_c) % 2).astype(np.uint8)
            if pred.size == 1:
                predictions[i, 0] = pred[0] & 1

        return predictions

    def _decode_target(self, sx):
        if not sx.any():
            return None
        key = sx.tobytes()
        if self._tgt_lookup is not None:
            entry = self._tgt_lookup.get(key)
            if entry is not None:
                _, indices = entry
                corr = np.zeros(len(self._tgt_map), dtype=np.uint8)
                for j in indices:
                    if j < len(corr): corr[j] = 1
                return corr
        return self._tgt_bposd.decode(sx)
