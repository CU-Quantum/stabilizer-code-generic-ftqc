import numpy as np
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
    edge_priors = np.zeros(n_edges)
    for m in range(h2e.shape[1]):
        ps = h2e[:, m].toarray().flatten()
        edge_indices = np.where(ps > 0)[0]
        if len(edge_indices) == 0:
            continue
        pm = priors[m]
        for ei, e in enumerate(edge_indices):
            pc = pm * ps[e]
            if ei > 0:
                pc *= (1.0 - pm) if pm < 0.5 else 1.0
            edge_priors[e] = 1.0 - (1.0 - edge_priors[e]) * (1.0 - pc)
    edge_priors = np.clip(edge_priors, 1e-300, 1.0 - 1e-300)
    return np.log((1.0 - edge_priors) / edge_priors)


def _build_matcher(edge_cm, h2e, priors, detector_mask):
    sub_cm, col_map = _filter_rows_cols(edge_cm, detector_mask)
    if sub_cm.shape[1] == 0:
        return None, col_map, np.array([])
    all_edge_weights = _edge_weights_from_priors(h2e, priors)
    sub_weights = all_edge_weights[col_map]
    return pymatching.Matching(sub_cm, weights=sub_weights), col_map, sub_weights


class _ExactMwDecoder:
    """Exact MWPM on mechanism-level matrix, falls back to weighted pymatching."""

    def __init__(self, cm, obs, priors, matcher, edge_obs):
        cm = cm.tocsc()
        obs = obs.toarray().astype(np.uint8) if hasattr(obs, 'toarray') else np.array(obs, dtype=np.uint8)
        self._priors = np.array(priors)
        self._n_det, self._n_mech = cm.shape
        self._n_obs = obs.shape[0]
        self._columns = [cm[:, i].toarray().flatten().astype(np.uint8) for i in range(self._n_mech)]
        self._obs_cols = [obs[:, i] for i in range(self._n_mech)]
        self._matcher = matcher
        self._edge_obs = edge_obs
        self._cache = {}
        self._low_weight_table = self._build_low_weight_table()

    def _build_low_weight_table(self):
        table = {}
        log_priors = np.log(np.clip(self._priors, 1e-300, None))
        for i in range(self._n_mech):
            key = (1, self._columns[i].tobytes())
            prob = np.exp(log_priors[i])
            existing = table.get(key)
            if existing is None or prob > existing[1]:
                table[key] = ([i], prob)
        for i in range(self._n_mech):
            for j in range(i + 1, self._n_mech):
                syn = self._columns[i] ^ self._columns[j]
                key = (2, syn.tobytes())
                prob = np.exp(log_priors[i] + log_priors[j])
                existing = table.get(key)
                if existing is None or prob > existing[1]:
                    table[key] = ([i, j], prob)
        return table

    def _make_correction(self, indices):
        corr = np.zeros(self._n_mech, dtype=np.uint8)
        for idx in indices:
            corr[idx] = 1
        return corr

    def _obs_from_corr(self, corr):
        pred = np.zeros(self._n_obs, dtype=np.uint8)
        for i in np.where(corr)[0]:
            if i < self._n_mech:
                pred ^= self._obs_cols[i]
        return pred

    def decode(self, sx):
        if not sx.any():
            return 0, None
        key = sx.tobytes()
        cached = self._cache.get(key)
        if cached is not None:
            return cached

        w = int(np.sum(sx))

        if w <= 3:
            for wt in (1, 2):
                entry = self._low_weight_table.get((wt, key))
                if entry is not None:
                    indices, _ = entry
                    corr = self._make_correction(indices)
                    pred = int(self._obs_from_corr(corr)[0] & 1)
                    result = (pred, corr)
                    if len(self._cache) < 10_000_000:
                        self._cache[key] = result
                    return result

            for m in range(min(self._n_mech, 3000)):
                residual_key = (2, (sx ^ self._columns[m]).tobytes())
                entry = self._low_weight_table.get(residual_key)
                if entry is not None:
                    indices, _ = entry
                    all_indices = [m] + indices
                    corr = self._make_correction(all_indices)
                    pred = int(self._obs_from_corr(corr)[0] & 1)
                    result = (pred, corr)
                    if len(self._cache) < 10_000_000:
                        self._cache[key] = result
                    return result

        if self._matcher is not None:
            fault_pred = self._matcher.decode(sx)
            pred = int((self._edge_obs @ fault_pred) % 2)
            result = (pred, None)
            if len(self._cache) < 10_000_000:
                self._cache[key] = result
            return result

        return 0, None


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
        obs = matrices.observables_matrix
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

        edge_cm = matrices.edge_check_matrix.tocsc()
        h2e = matrices.hyperedge_to_edge_matrix
        edge_obs = matrices.edge_observables_matrix.toarray().astype(np.uint8)

        tgt_cm, tgt_map = _filter_rows_cols(cm, is_target)
        tgt_matcher, tgt_edge_map, _ = _build_matcher(edge_cm, h2e, priors, is_target)
        tgt_edge_obs = edge_obs[:, tgt_edge_map] if tgt_matcher is not None else np.array([])
        tgt_priors = [priors[c] for c in tgt_map]
        tgt_obs = obs[:, tgt_map]
        tgt_decoder = _ExactMwDecoder(tgt_cm, tgt_obs, tgt_priors, tgt_matcher, tgt_edge_obs)

        ctrl_cm, ctrl_map = _filter_rows_cols(cm, ~is_target)
        ctrl_matcher, ctrl_edge_map, _ = _build_matcher(edge_cm, h2e, priors, ~is_target)
        ctrl_edge_obs = edge_obs[:, ctrl_edge_map] if ctrl_matcher is not None else np.array([])
        ctrl_priors = [priors[c] for c in ctrl_map]
        ctrl_obs = obs[:, ctrl_map]
        ctrl_decoder = _ExactMwDecoder(ctrl_cm, ctrl_obs, ctrl_priors, ctrl_matcher, ctrl_edge_obs)

        modified_det_indices = None
        if has_cx:
            modified_det_indices = _compute_modified_detector_indices(
                num_gens, num_target, num_repeats, self._modified_index)

        return CompiledPartitionDecoder(
            tgt_decoder=tgt_decoder,
            ctrl_decoder=ctrl_decoder,
            num_detectors=num_detectors,
            is_target=is_target,
            has_cx=has_cx,
            modified_det_indices=modified_det_indices,
        )


def _compute_modified_detector_indices(num_gens, num_target, num_repeats, modified_index):
    n_ctrl = num_gens - num_target
    ctrl_modified_offset = modified_index - num_target
    indices = []
    for r in range(num_repeats):
        pos = r * n_ctrl + ctrl_modified_offset
        indices.append(pos)
    return np.array(indices, dtype=int)


class _EmptyDecoder(CompiledDecoder):
    def __init__(self, n_det, n_obs):
        self._nd = n_det; self._no = n_obs
    def decode_shots_bit_packed(self, *, bit_packed_detection_event_data):
        u = np.unpackbits(bit_packed_detection_event_data, axis=1, bitorder='little')
        return np.zeros((u.shape[0], (self._no + 7) // 8), dtype=np.uint8)


class CompiledPartitionDecoder(CompiledDecoder):
    def __init__(self, tgt_decoder, ctrl_decoder,
                 num_detectors, is_target, has_cx, modified_det_indices):
        self._tgt_decoder = tgt_decoder
        self._ctrl_decoder = ctrl_decoder
        self._num_detectors = num_detectors
        self._is_target = is_target
        self._has_cx = has_cx
        self._modified_det_indices = modified_det_indices

    def decode_shots_bit_packed(self, *, bit_packed_detection_event_data):
        unpacked = np.unpackbits(bit_packed_detection_event_data, axis=1,
                                 bitorder='little')[:, :self._num_detectors]
        num_shots = unpacked.shape[0]
        predictions = np.zeros((num_shots, 1), dtype=np.uint8)

        td = unpacked[:, self._is_target]
        cd_raw = unpacked[:, ~self._is_target]

        for i in range(num_shots):
            ts = td[i].astype(np.uint8)
            cs = cd_raw[i].copy().astype(np.uint8)

            if not ts.any() and not cs.any():
                continue

            tgt_pred, _ = self._tgt_decoder.decode(ts)

            if self._has_cx and self._modified_det_indices is not None and tgt_pred:
                for idx in self._modified_det_indices:
                    if idx < len(cs):
                        cs[idx] ^= 1

            ctrl_pred, _ = self._ctrl_decoder.decode(cs)

            predictions[i, 0] = tgt_pred ^ ctrl_pred

        return predictions
