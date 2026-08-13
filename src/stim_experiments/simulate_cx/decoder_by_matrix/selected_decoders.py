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
from scipy.optimize import Bounds, LinearConstraint, milp
from scipy.sparse import coo_matrix


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


class IlpMwDecoder(_MechanismDecoder):
    """Exact minimum-weight decoder via integer linear programming.

    Solves, for a given syndrome s,

        min  sum_j (-log prior_j) x_j
        s.t. cm @ x = s  (mod 2),  x_j in {0, 1}

    where ``cm`` is the check matrix (each column an error mechanism) and the
    priors are the mechanism probabilities.  The mod-2 constraints are
    expressed as ``cm @ x - 2 k = s`` with integer slack variables ``k`` and
    handed to the HiGHS solver (via ``scipy.optimize.milp``).  This is the
    exact maximum-a-posteriori decoder, which BP-OSD approximates but does not
    attain for dense non-CSS codes such as [[17,1,7]].
    """

    def __init__(self, cm, obs, priors, x_obs=None):
        super().__init__(cm, obs, priors, x_obs=x_obs)
        self._cache = {}
        cm_dense = cm.toarray().astype(np.uint8)
        self._n_det, self._n_mech = cm_dense.shape
        weights = -np.log(np.clip(self._priors, 1e-300, None))
        self._objective = np.concatenate([weights, np.zeros(self._n_det)])
        self._integrality = np.ones(self._n_mech + self._n_det)
        self._bounds = Bounds(
            np.concatenate([np.zeros(self._n_mech), np.zeros(self._n_det)]),
            np.concatenate([np.ones(self._n_mech), np.full(self._n_det, np.inf)]),
        )
        rows = []
        cols = []
        data = []
        for i in range(self._n_det):
            for j in range(self._n_mech):
                if cm_dense[i, j]:
                    rows.append(i)
                    cols.append(j)
                    data.append(1)
            rows.append(i)
            cols.append(self._n_mech + i)
            data.append(-2)
        self._constraint_matrix = coo_matrix(
            (data, (rows, cols)), shape=(self._n_det, self._n_mech + self._n_det)
        ).tocsr()

        # Fast exact low-weight pre-filter (weight 1/2/3/4) so the MILP is only
        # invoked for the rare syndromes whose minimum-weight explanation has
        # weight >= 5.  This is exact: it returns the same MAP error the MILP
        # would for weight <= 4 syndromes.  ``_w2`` stores the top-2 pairs per
        # syndrome so the meet-in-the-middle searches can skip an overlapping
        # pair without losing the exact MAP answer.
        self._cols_int = []
        for j in range(self._n_mech):
            v = 0
            for d in np.where(cm_dense[:, j])[0]:
                v |= 1 << int(d)
            self._cols_int.append(v)
        self._w1 = {}
        for j in range(self._n_mech):
            key = self._cols_int[j]
            cur = self._w1.get(key)
            if cur is None or self._priors[j] > self._priors[cur]:
                self._w1[key] = j
        self._w2 = {}
        for j in range(self._n_mech):
            for k in range(j + 1, self._n_mech):
                key = self._cols_int[j] ^ self._cols_int[k]
                lp = self._log_priors[j] + self._log_priors[k]
                lst = self._w2.get(key)
                if lst is None:
                    self._w2[key] = [(lp, (j, k))]
                elif len(lst) < 2:
                    lst.append((lp, (j, k)))
                    if lst[0][0] < lst[1][0]:
                        lst[0], lst[1] = lst[1], lst[0]
                elif lp > lst[1][0]:
                    lst[1] = (lp, (j, k))
                    if lst[0][0] < lst[1][0]:
                        lst[0], lst[1] = lst[1], lst[0]

    @staticmethod
    def _pack(sx):
        v = 0
        for d in np.where(sx)[0]:
            v |= 1 << int(d)
        return v

    def _best_weight(self, target, extra, extra_lp):
        """Best explanation of ``target`` using ``extra`` mechanisms plus a w2 pair.

        ``extra`` is a tuple of mechanism indices already chosen (their log
        priors summed in ``extra_lp``); the remaining syndrome is matched with
        a stored weight-2 pair.  Returns (lp, [indices]) or None.
        """
        lst = self._w2.get(target)
        if lst is None:
            return None
        best = None
        for pair_lp, (a, b) in lst:
            if a in extra or b in extra:
                continue
            lp = extra_lp + pair_lp
            if best is None or lp > best[0]:
                best = (lp, list(extra) + [a, b])
        return best

    def _weight4(self, target):
        """Weight-4 meet-in-the-middle; returns [indices] or None."""
        best = None
        best_lp = -np.inf
        for i in range(self._n_mech):
            ci = self._cols_int[i]
            lpi = self._log_priors[i]
            for j in range(i + 1, self._n_mech):
                lst = self._w2.get(target ^ ci ^ self._cols_int[j])
                if lst is None:
                    continue
                base_lp = lpi + self._log_priors[j]
                for pair_lp, (a, b) in lst:
                    if a == i or b == i or a == j or b == j:
                        continue
                    lp = base_lp + pair_lp
                    if lp > best_lp:
                        best_lp = lp
                        best = [i, j, a, b]
        return best

    def _fast_low_weight(self, sx):
        """Return the MAP correction for syndromes of min weight <= 4, else None."""
        target = self._pack(sx)
        j = self._w1.get(target)
        if j is not None:
            return self._make_correction([j])
        lst = self._w2.get(target)
        if lst is not None:
            return self._make_correction(list(lst[0][1]))
        best = None
        for j in range(self._n_mech):
            cand = self._best_weight(target ^ self._cols_int[j], (j,),
                                     self._log_priors[j])
            if cand is not None and (best is None or cand[0] > best[0]):
                best = cand
        if best is not None:
            return self._make_correction(best[1])
        idx4 = self._weight4(target)
        if idx4 is not None:
            return self._make_correction(idx4)
        return None

    def decode(self, sx):
        if not sx.any():
            return 0, None, 0
        key = sx.tobytes()
        result = self._cache.get(key)
        if result is None:
            result = self._decode_uncached(sx)
            self._cache[key] = result
        return result

    def _decode_uncached(self, sx):
        corr = self._fast_low_weight(sx)
        if corr is None:
            corr = self._solve_ilp(sx)
        if corr is None:
            return 0, None, 0
        pred = int(self._obs_from_corr(corr)[0] & 1)
        x_pred = self._x_from_corr(corr)
        return pred, corr, x_pred

    def _solve_ilp(self, sx):
        res = milp(
            c=self._objective,
            integrality=self._integrality,
            bounds=self._bounds,
            constraints=LinearConstraint(
                self._constraint_matrix, sx.astype(float), sx.astype(float)
            ),
        )
        if not res.success:
            return None
        return np.round(res.x[: self._n_mech]).astype(np.uint8)
