"""Selected per-partition decoders used by the standalone partition decoder.

Each decoder exposes the same interface expected by the standalone partition
decoder:

    decode(sx) -> (pred, corr, x_pred)
    get_x_changes(sx, num_rounds) -> np.ndarray (per-round X changes)

where ``pred`` is the partition's logical-observable prediction, ``corr`` is a
correction vector over the partition's error mechanisms (may be ``None`` for
matching decoders), and ``x_pred`` flags whether the correction flips the
partition's X (bridge) observable.
"""

import numpy as np
from ldpc.bposd_decoder import BpOsdDecoder as LdpcBpOsdDecoder


def _dot(obs, vec):
    if obs is None or obs.size == 0:
        return 0
    d = (obs @ vec) % 2
    return int(d.flat[0]) if d.ndim > 0 else int(d)


class MwpmDecoder:
    """Minimum-weight perfect-matching (pymatching) decoder."""

    def __init__(self, matcher, edge_obs, n_det=None, edge_x_obs=None, edge_to_round=None):
        self._matcher = matcher
        self._edge_obs = edge_obs
        self._edge_x_obs = edge_x_obs
        self._edge_to_round = edge_to_round
        self._n_det = n_det if n_det is not None else (matcher.num_detectors if matcher is not None else 0)

    def decode(self, sx):
        if not sx.any() or self._matcher is None:
            return 0, None, 0
        fault_pred = self._matcher.decode(sx)
        pred = _dot(self._edge_obs, fault_pred)
        x_pred = _dot(self._edge_x_obs, fault_pred) if self._edge_x_obs is not None else 0
        return pred, None, x_pred

    def get_x_changes(self, sx, num_rounds):
        if self._edge_x_obs is None or self._edge_to_round is None:
            return np.zeros(num_rounds, dtype=np.uint8)
        if not sx.any() or self._matcher is None:
            return np.zeros(num_rounds, dtype=np.uint8)
        fault_pred = self._matcher.decode(sx)
        changes = np.zeros(num_rounds, dtype=np.uint8)
        for e in np.where(fault_pred > 0)[0]:
            if e < self._edge_x_obs.shape[1] and self._edge_x_obs[0, e]:
                r = self._edge_to_round.get(e)
                if r is not None and r < num_rounds:
                    changes[r] ^= 1
        return changes


class _MechanismDecoder:
    """Shared machinery for decoders that produce corrections over mechanisms."""

    def __init__(self, cm, obs, priors, x_obs=None):
        cm = cm.tocsc()
        obs = obs.toarray().astype(np.uint8) if hasattr(obs, 'toarray') else np.array(obs, dtype=np.uint8)
        self._priors = np.array(priors)
        self._n_det, self._n_mech = cm.shape
        self._columns = [cm[:, i].toarray().flatten().astype(np.uint8) for i in range(self._n_mech)]
        self._obs_cols = [obs[:, i] for i in range(self._n_mech)]
        self._x_obs_cols = None
        if x_obs is not None:
            self._x_obs_cols = [x_obs[:, i] for i in range(x_obs.shape[1])]
        self._mech_x_to_round = None
        self._log_priors = np.log(np.clip(self._priors, 1e-300, None))

    def _make_correction(self, indices):
        corr = np.zeros(self._n_mech, dtype=np.uint8)
        for idx in indices:
            corr[idx] = 1
        return corr

    def _obs_from_corr(self, corr):
        pred = np.zeros(1, dtype=np.uint8)
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

    def get_x_changes(self, sx, num_rounds):
        changes = np.zeros(num_rounds, dtype=np.uint8)
        _, corr, _ = self.decode(sx)
        if corr is None or self._mech_x_to_round is None or self._x_obs_cols is None:
            return changes
        for i in np.where(corr > 0)[0]:
            if i < len(self._x_obs_cols) and self._x_obs_cols[i].flat[0]:
                r = self._mech_x_to_round.get(i)
                if r is not None and r < num_rounds:
                    changes[r] ^= 1
        return changes


class SingleErrorLookupDecoder(_MechanismDecoder):
    """Exact single-error lookup table (for distance-3 codes such as [[5,1,3]])."""

    def __init__(self, cm, obs, priors, x_obs=None):
        super().__init__(cm, obs, priors, x_obs=x_obs)
        self._table = {}
        for i in range(self._n_mech):
            key = self._columns[i].tobytes()
            prob = float(np.exp(self._log_priors[i]))
            existing = self._table.get(key)
            if existing is None or prob > existing[1]:
                self._table[key] = ([i], prob)

    def decode(self, sx):
        if not sx.any():
            return 0, None, 0
        entry = self._table.get(sx.tobytes())
        if entry is None:
            return 0, None, 0
        indices, _ = entry
        corr = self._make_correction(indices)
        pred = int(self._obs_from_corr(corr)[0] & 1)
        x_pred = self._x_from_corr(corr)
        return pred, corr, x_pred


class BpOsdDecoder(_MechanismDecoder):
    """Belief-propagation + ordered-statistics decoding (near-optimal for small codes)."""

    def __init__(self, cm, obs, priors, x_obs=None, max_iter=100,
                 osd_method='osd_cs', osd_order=40):
        super().__init__(cm, obs, priors, x_obs=x_obs)
        self._bposd = LdpcBpOsdDecoder(
            cm,
            error_channel=list(priors),
            max_iter=max_iter,
            bp_method='ms',
            ms_scaling_factor=0.625,
            schedule='parallel',
            osd_method=osd_method,
            osd_order=osd_order,
        )

    def decode(self, sx):
        if not sx.any():
            return 0, None, 0
        corr = self._bposd.decode(sx)
        if corr is None:
            return 0, None, 0
        pred = int(self._obs_from_corr(corr)[0] & 1)
        x_pred = self._x_from_corr(corr)
        return pred, corr, x_pred


class GraphAwareBoundedDistanceDecoder(_MechanismDecoder):
    """Bounded-distance decoder via exact minimum-weight enumeration.

    Finds the most-likely error of weight at most
    ``floor((distance - 1) / 2)`` whose syndrome matches the observed one, using
    a meet-in-the-middle syndrome lookup so that weight-2/3 searches do not
    require exhaustive pair/triple enumeration per syndrome.
    """

    def __init__(self, cm, obs, priors, distance, x_obs=None):
        super().__init__(cm, obs, priors, x_obs=x_obs)
        self._t = (distance - 1) // 2
        self._cols = [self._pack(self._columns[i]) for i in range(self._n_mech)]
        self._syn_to_mechs = {}
        for i in range(self._n_mech):
            self._syn_to_mechs.setdefault(int(self._cols[i]), []).append(i)

    @staticmethod
    def _pack(vec):
        v = 0
        for d in np.where(vec)[0]:
            v |= 1 << int(d)
        return v

    def decode(self, sx):
        if not sx.any():
            return 0, None, 0
        target = int(self._pack(sx))
        n = self._n_mech
        best = None

        for idx in self._syn_to_mechs.get(target, []):
            lp = float(self._log_priors[idx])
            if best is None or lp > best[0]:
                best = (lp, [idx])
        if best is not None:
            return self._result(best[1])

        if self._t >= 2:
            for i in range(n):
                lst = self._syn_to_mechs.get(target ^ int(self._cols[i]))
                if not lst:
                    continue
                for j in lst:
                    if j <= i:
                        continue
                    lp = float(self._log_priors[i] + self._log_priors[j])
                    if best is None or lp > best[0]:
                        best = (lp, [i, j])
            if best is not None:
                return self._result(best[1])

        if self._t >= 3:
            for i in range(n):
                ci = int(self._cols[i])
                for j in range(i + 1, n):
                    lst = self._syn_to_mechs.get(target ^ ci ^ int(self._cols[j]))
                    if not lst:
                        continue
                    for k in lst:
                        if k <= j:
                            continue
                        lp = float(self._log_priors[i] + self._log_priors[j] + self._log_priors[k])
                        if best is None or lp > best[0]:
                            best = (lp, [i, j, k])
            if best is not None:
                return self._result(best[1])

        return 0, None, 0

    def _result(self, indices):
        corr = self._make_correction(indices)
        pred = int(self._obs_from_corr(corr)[0] & 1)
        x_pred = self._x_from_corr(corr)
        return pred, corr, x_pred
