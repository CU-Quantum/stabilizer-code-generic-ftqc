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


def _edge_weights_from_priors(h2e, priors):
    h2e = h2e.tocsc()
    n_edges = h2e.shape[0]
    n_mech = h2e.shape[1]
    edge_priors = np.zeros(n_edges)
    for m in range(n_mech):
        ps = h2e[:, m].toarray().flatten()
        edge_indices = np.where(ps > 0)[0]
        if len(edge_indices) == 0:
            continue
        pm = priors[m]
        for ei, e in enumerate(edge_indices):
            p_contribution = pm * ps[e]
            if ei > 0:
                p_contribution *= (1.0 - pm) if pm < 0.5 else 1.0
            edge_priors[e] = 1.0 - (1.0 - edge_priors[e]) * (1.0 - p_contribution)
    edge_priors = np.clip(edge_priors, 1e-300, 1.0 - 1e-300)
    return np.log((1.0 - edge_priors) / edge_priors)


def _build_matcher(edge_cm, h2e, priors, detector_mask):
    sub_cm, col_map = _filter_rows_cols(edge_cm, detector_mask)
    if sub_cm.shape[1] == 0:
        return None, col_map
    all_edge_weights = _edge_weights_from_priors(h2e, priors)
    sub_weights = all_edge_weights[col_map]
    return pymatching.Matching(sub_cm, weights=sub_weights), col_map


def _build_exact_correction_lookup(tgt_cm, tgt_obs, tgt_priors):
    n_mech = tgt_cm.shape[1]
    tgt_cm = tgt_cm.tocsc()
    columns = [tgt_cm[:, i].toarray().flatten().astype(np.uint8) for i in range(n_mech)]
    obs_cols = [tgt_obs[:, i] for i in range(n_mech)]

    low_weight_table = {}

    for i in range(n_mech):
        key = (1, columns[i].tobytes())
        entry = low_weight_table.get(key)
        if entry is None or tgt_priors[i] > entry[1]:
            low_weight_table[key] = (np.array([i]), tgt_priors[i])

    for i in range(n_mech):
        for j in range(i + 1, n_mech):
            syn = columns[i] ^ columns[j]
            key = (2, syn.tobytes())
            prob = tgt_priors[i] * tgt_priors[j]
            entry = low_weight_table.get(key)
            if entry is None or prob > entry[1]:
                low_weight_table[key] = (np.array([i, j]), prob)

    return low_weight_table, columns, obs_cols


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
        has_cx = (self._modified_index is not None)

        is_target = np.zeros(num_detectors, dtype=bool)
        for r in range(num_repeats):
            is_target[r * num_gens:(r * num_gens) + num_target] = True

        tgt_cm, tgt_map = _filter_rows_cols(cm, is_target)
        tgt_priors = [priors[c] for c in tgt_map]
        tgt_obs = obs[:, tgt_map]

        tgt_bposd = None
        tgt_matcher = None
        tgt_edge_obs = None
        tgt_lookup = None
        tgt_exact_low_weight = None
        tgt_exact_columns = None
        tgt_exact_obs_cols = None

        edge_cm = matrices.edge_check_matrix.tocsc()
        h2e = matrices.hyperedge_to_edge_matrix
        edge_obs = matrices.edge_observables_matrix.toarray().astype(np.uint8)

        if self._target_decoder in ('bposd', 'lookup'):
            tgt_bposd = BpOsdDecoder(
                tgt_cm, error_channel=tgt_priors,
                max_iter=100, bp_method='ms', ms_scaling_factor=0.625,
                schedule='parallel', osd_method='osd_cs', osd_order=10,
            )
            if self._target_decoder == 'lookup':
                tgt_lookup = _build_lookup_table(tgt_cm, tgt_obs, self._distance)
        elif self._target_decoder == 'mwpm':
            tgt_bposd = BpOsdDecoder(
                tgt_cm, error_channel=tgt_priors,
                max_iter=100, bp_method='ms', ms_scaling_factor=0.625,
                schedule='parallel', osd_method='osd_cs', osd_order=10,
            )
            tgt_matcher, tgt_edge_map = _build_matcher(edge_cm, h2e, priors, is_target)
            tgt_edge_obs = edge_obs[:, tgt_edge_map]
            tgt_lookup = _build_lookup_table(tgt_cm, tgt_obs, self._distance)
            tgt_exact_low_weight, tgt_exact_columns, tgt_exact_obs_cols = \
                _build_exact_correction_lookup(tgt_cm, tgt_obs, tgt_priors)

        ctrl_matcher, ctrl_edge_map = _build_matcher(edge_cm, h2e, priors, ~is_target)
        ctrl_edge_obs = edge_obs[:, ctrl_edge_map] if ctrl_matcher is not None else None

        modified_det_indices = None
        if has_cx:
            modified_det_indices = _compute_modified_detector_indices(
                num_gens, num_target, num_repeats, self._modified_index)

        return CompiledPartitionDecoder(
            tgt_bposd=tgt_bposd,
            tgt_matcher=tgt_matcher,
            tgt_edge_obs=tgt_edge_obs,
            tgt_obs=tgt_obs,
            tgt_lookup=tgt_lookup,
            tgt_map=tgt_map,
            tgt_exact_low_weight=tgt_exact_low_weight,
            tgt_exact_columns=tgt_exact_columns,
            tgt_exact_obs_cols=tgt_exact_obs_cols,
            ctrl_matcher=ctrl_matcher,
            ctrl_edge_obs=ctrl_edge_obs,
            full_cm=cm,
            full_obs=obs,
            num_detectors=num_detectors,
            is_target=is_target,
            has_cx=has_cx,
            modified_det_indices=modified_det_indices,
            target_decoder=self._target_decoder,
        )


def _compute_modified_detector_indices(num_gens, num_target, num_repeats, modified_index):
    n_ctrl = num_gens - num_target
    ctrl_modified_offset = modified_index - num_target
    indices = []
    for r in range(num_repeats):
        pos = r * n_ctrl + ctrl_modified_offset
        indices.append(pos)
    return np.array(indices, dtype=int)


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
    def __init__(self, tgt_bposd, tgt_matcher, tgt_edge_obs,
                 tgt_obs, tgt_lookup, tgt_map,
                 tgt_exact_low_weight, tgt_exact_columns, tgt_exact_obs_cols,
                 ctrl_matcher, ctrl_edge_obs,
                 full_cm, full_obs,
                 num_detectors, is_target, has_cx,
                 modified_det_indices, target_decoder):
        self._tgt_bposd = tgt_bposd
        self._tgt_matcher = tgt_matcher
        self._tgt_edge_obs = tgt_edge_obs
        self._tgt_obs = tgt_obs
        self._tgt_lookup = tgt_lookup
        self._tgt_map = tgt_map
        self._tgt_exact_low_weight = tgt_exact_low_weight
        self._tgt_exact_columns = tgt_exact_columns
        self._tgt_exact_obs_cols = tgt_exact_obs_cols
        self._ctrl_matcher = ctrl_matcher
        self._ctrl_edge_obs = ctrl_edge_obs
        self._full_cm = full_cm
        self._full_obs = full_obs
        self._num_detectors = num_detectors
        self._is_target = is_target
        self._has_cx = has_cx
        self._modified_det_indices = modified_det_indices
        self._target_decoder = target_decoder
        self._n_mech = len(tgt_map)

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

            tgt_pred, tgt_corr = self._decode_target(ts)

            if tgt_corr is not None and self._has_cx:
                full_c = np.zeros(self._full_cm.shape[1], dtype=np.uint8)
                for j, col in enumerate(self._tgt_map):
                    full_c[col] = tgt_corr[j]
                contrib = (self._full_cm[~self._is_target, :] @ full_c) % 2
                cs ^= contrib.astype(np.uint8)

            if self._has_cx and self._modified_det_indices is not None and tgt_pred:
                for idx in self._modified_det_indices:
                    if idx < len(cs):
                        cs[idx] ^= 1

            ctrl_pred = 0
            if cs.any() and self._ctrl_matcher is not None:
                ctrl_pred = self._decode_control(cs)

            predictions[i, 0] = tgt_pred ^ ctrl_pred

        return predictions

    def _decode_target(self, sx):
        if not sx.any():
            return 0, None
        key = sx.tobytes()

        if self._tgt_lookup is not None:
            entry = self._tgt_lookup.get(key)
            if entry is not None:
                pred, indices = entry
                corr = np.zeros(len(self._tgt_map), dtype=np.uint8)
                for j in indices:
                    if j < len(corr): corr[j] = 1
                return int(pred[0] & 1), corr

        corr = self._compute_exact_correction(sx, key)
        if corr is not None:
            obs_pred = int((self._tgt_obs @ corr) % 2)
            return obs_pred, corr

        if self._tgt_matcher is not None:
            fault_pred = self._tgt_matcher.decode(sx)
            obs_pred = int((self._tgt_edge_obs @ fault_pred) % 2)
            corr = self._tgt_bposd.decode(sx)
            return obs_pred, corr

        if self._tgt_bposd is not None:
            corr = self._tgt_bposd.decode(sx)
            if corr is not None:
                pred = int((self._tgt_obs @ corr) % 2)
                return pred, corr

        return 0, None

    def _compute_exact_correction(self, sx, key):
        if self._tgt_exact_low_weight is None:
            return None

        for weight in (1, 2):
            entry = self._tgt_exact_low_weight.get((weight, key))
            if entry is not None:
                indices, _ = entry
                corr = np.zeros(self._n_mech, dtype=np.uint8)
                for j in indices:
                    if j < self._n_mech: corr[j] = 1
                return corr

        for m in range(self._n_mech):
            residual_key = (2, (sx ^ self._tgt_exact_columns[m]).tobytes())
            entry = self._tgt_exact_low_weight.get(residual_key)
            if entry is not None:
                indices, _ = entry
                corr = np.zeros(self._n_mech, dtype=np.uint8)
                corr[m] = 1
                for j in indices:
                    if j < self._n_mech: corr[j] = 1
                return corr

        return None

    def _decode_control(self, sx):
        if not sx.any():
            return 0
        fault_pred = self._ctrl_matcher.decode(sx)
        return int((self._ctrl_edge_obs @ fault_pred) % 2)
