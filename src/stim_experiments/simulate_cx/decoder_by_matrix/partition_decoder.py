import numpy as np
from ldpc.bposd_decoder import BpOsdDecoder
from ldpc.ckt_noise import detector_error_model_to_check_matrices
from sinter import CompiledDecoder, Decoder
import pymatching


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

        # --- Control MWPM via pymatching (edge-level matching) ---
        edge_cm = matrices.edge_check_matrix.tocsc()
        ctrl_edge_cm, _ctrl_edge_map = _filter_rows_cols(edge_cm, ~is_target)
        ctrl_edge_priors_vec = np.array(matrices.priors)
        if ctrl_edge_cm.shape[1] > 0:
            ctrl_matcher = pymatching.Matching(ctrl_edge_cm)
        else:
            ctrl_matcher = None

        return CompiledPartitionDecoder(
            tgt_bposd=tgt_bposd, tgt_obs=tgt_obs, tgt_lookup=tgt_lookup,
            tgt_map=tgt_map, ctrl_matcher=ctrl_matcher,
            full_cm=cm, full_obs=obs,
            num_detectors=num_detectors,
            is_target=is_target,
            has_cx=(self._modified_index is not None),
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
                 ctrl_matcher, full_cm, full_obs,
                 num_detectors, is_target, has_cx):
        self._tgt_bposd = tgt_bposd
        self._tgt_obs = tgt_obs
        self._tgt_lookup = tgt_lookup
        self._tgt_map = tgt_map
        self._ctrl_matcher = ctrl_matcher
        self._full_cm = full_cm
        self._full_obs = full_obs
        self._num_detectors = num_detectors
        self._is_target = is_target
        self._has_cx = has_cx

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

            # Step 1: decode target (BP-OSD)
            tgt_corr = self._decode_target(ts)

            # Compute target observable prediction
            tgt_pred = 0
            if tgt_corr is not None:
                tgt_pred = int((self._tgt_obs @ tgt_corr) % 2)

            # Step 2: subtract target contribution from control syndrome
            if tgt_corr is not None and self._has_cx:
                full_c = np.zeros(self._full_cm.shape[1], dtype=np.uint8)
                for j, col in enumerate(self._tgt_map):
                    full_c[col] = tgt_corr[j]
                contrib = (self._full_cm[~self._is_target, :] @ full_c) % 2
                cs ^= contrib.astype(np.uint8)

            # Step 3: decode control via MWPM (returns observable prediction)
            ctrl_pred = 0
            if cs.any() and self._ctrl_matcher is not None:
                ctrl_pred = int(self._ctrl_matcher.decode(cs) % 2)

            # Step 4: XOR predictions
            predictions[i, 0] = tgt_pred ^ ctrl_pred

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
