import numpy as np
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
    def __init__(self, cm, obs, priors, matcher, edge_obs, x_obs=None, bposd=None):
        cm = cm.tocsc()
        obs = obs.toarray().astype(np.uint8) if hasattr(obs, 'toarray') else np.array(obs, dtype=np.uint8)
        self._priors = np.array(priors)
        self._n_det, self._n_mech = cm.shape
        self._n_obs = obs.shape[0]
        self._columns = [cm[:, i].toarray().flatten().astype(np.uint8) for i in range(self._n_mech)]
        self._obs_cols = [obs[:, i] for i in range(self._n_mech)]
        self._x_obs_cols = None
        if x_obs is not None:
            self._x_obs_cols = [x_obs[:, i] for i in range(x_obs.shape[1])]
        self._matcher = matcher
        self._bposd = bposd
        self._edge_obs = edge_obs
        self._cache = {}
        self._low_weight_table = self._build_low_weight_table()
        self._edge_x_obs = None
        self._edge_to_round = None
        self._mech_x_to_round = None

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

    def _x_from_corr(self, corr):
        if self._x_obs_cols is None:
            return 0
        pred = 0
        for i in np.where(corr)[0]:
            if i < len(self._x_obs_cols):
                pred ^= int(self._x_obs_cols[i].flat[0])
        return pred

    def decode(self, sx):
        if not sx.any():
            return 0, None, 0
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
                    x_pred = self._x_from_corr(corr)
                    result = (pred, corr, x_pred)
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
                    x_pred = self._x_from_corr(corr)
                    result = (pred, corr, x_pred)
                    if len(self._cache) < 10_000_000:
                        self._cache[key] = result
                    return result

        if self._bposd is not None:
            corr = self._bposd.decode(sx)
            pred = int(self._obs_from_corr(corr)[0] & 1)
            x_pred = self._x_from_corr(corr)
            result = (pred, corr, x_pred)
            if len(self._cache) < 10_000_000:
                self._cache[key] = result
            return result

        if self._matcher is not None:
            fault_pred = self._matcher.decode(sx)
            edge_dot = (self._edge_obs @ fault_pred) % 2
            pred = int(edge_dot.flat[0]) if edge_dot.ndim > 0 else int(edge_dot)
            if self._edge_x_obs is not None:
                edge_x_dot = (self._edge_x_obs @ fault_pred) % 2
                x_pred = int(edge_x_dot.flat[0]) if edge_x_dot.ndim > 0 else int(edge_x_dot)
            else:
                x_pred = 0
            result = (pred, None, x_pred)
            if len(self._cache) < 10_000_000:
                self._cache[key] = result
            return result

        return 0, None, 0

    def get_x_changes(self, sx, num_rounds):
        if self._bposd is not None:
            corr = self._bposd.decode(sx)
            changes = np.zeros(num_rounds, dtype=np.uint8)
            if self._mech_x_to_round is not None and self._x_obs_cols is not None:
                for i in np.where(corr > 0)[0]:
                    if i < len(self._x_obs_cols) and self._x_obs_cols[i].flat[0]:
                        r = self._mech_x_to_round.get(i)
                        if r is not None and r < num_rounds:
                            changes[r] ^= 1
            return changes
        if self._matcher is None or self._edge_x_obs is None or self._edge_to_round is None:
            return np.zeros(num_rounds, dtype=np.uint8)
        if not sx.any():
            return np.zeros(num_rounds, dtype=np.uint8)
        fault_pred = self._matcher.decode(sx)
        changes = np.zeros(num_rounds, dtype=np.uint8)
        for e in np.where(fault_pred > 0)[0]:
            if e < self._edge_x_obs.shape[1] and self._edge_x_obs[0, e]:
                r = self._edge_to_round.get(e)
                if r is not None and r < num_rounds:
                    changes[r] ^= 1
        return changes
