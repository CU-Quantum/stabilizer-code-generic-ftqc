"""Standalone exact-MW partition decoder.

Builds a pure standalone decoder for the target code (from a single-code circuit)
and uses the combined DEM's control partition for the control decoder (to get
the correct partial observable).  Two-stage decoding with X-prediction bridge.
"""

import numpy as np
from sinter import CompiledDecoder, Decoder
from ldpc.ckt_noise import detector_error_model_to_check_matrices

from stim_experiments.simulate_cx.support.stabilizer_code_utilities import StabilizerCodeUtilities
from stim_experiments.simulate_cx.decoder_by_matrix.partition_decoder import (
    _build_matcher,
)
from stim_experiments.simulate_cx.decoder_by_matrix.selected_decoders import (
    MwpmDecoder,
    SingleErrorLookupDecoder,
    LookupTableDecoder,
    BpOsdDecoder,
)


def _estimate_p(priors):
    non_zero = sorted([pr for pr in priors if pr > 0])
    if not non_zero:
        return 0.01
    return 3 * np.median(non_zero[:max(1, len(non_zero) // 3)])


def _make_standalone_utils(utils):
    if utils._qubit_id_start != 0:
        return StabilizerCodeUtilities(
            symplectic_matrix=utils.symplectic_matrix,
            generator_anticommutators=utils._generator_anticommutators,
            z_observable=utils.z_observable,
            x_observable=utils.x_observable,
            target_code_utilities=utils._target_code_utilities,
            qubit_id_start=0,
            row_coord_start=utils.row_coord_start,
            existing_ancilla_indices=[],
        )
    return utils


def _compute_x_obs_from_combined(cm_combined, is_target_mask, modified_mask,
                                  tgt_cm_solo, num_target_per_round):
    """Match standalone target columns to combined columns to build x_obs.
    Also returns column mapping for full_cm projection."""
    n_standalone = tgt_cm_solo.shape[1]
    x_obs_vec = np.zeros(n_standalone, dtype=np.uint8)
    col_map = np.full(n_standalone, -1, dtype=int)

    target_rows_combined = cm_combined[is_target_mask, :].tocsc()
    modified_rows_combined = cm_combined[modified_mask, :].toarray()

    per_round_count = is_target_mask.sum()
    tgt_per_round = tgt_cm_solo[:per_round_count, :].tocsc()

    for j in range(n_standalone):
        sj = tgt_per_round[:, j].toarray().flatten()
        if not sj.any():
            continue
        for c in range(target_rows_combined.shape[1]):
            sc = target_rows_combined[:, c].toarray().flatten()
            if np.array_equal(sj, sc):
                col_map[j] = c
                if modified_rows_combined[:, c].any():
                    x_obs_vec[j] = 1
                break

    return x_obs_vec.reshape(1, -1), col_map


def _setup_edge_to_round(decoder, edge_cm, nt, num_rounds, edge_map):
    dets_per_round = nt
    per_round_mask = np.zeros(edge_cm.shape[0], dtype=bool)
    per_round_mask[:num_rounds * nt] = True
    edge_cm_per_round = edge_cm[per_round_mask, :][:, edge_map].tocsc()
    edge_to_round = {}
    for e in range(edge_cm_per_round.shape[1]):
        rows = edge_cm_per_round[:, e].toarray().flatten()
        nonzero = np.where(rows > 0)[0]
        if len(nonzero) > 0:
            r = int(nonzero[0]) // dets_per_round
            edge_to_round[e] = min(r, num_rounds - 1)
    decoder._edge_to_round = edge_to_round


def _setup_mech_x_to_round(decoder, cm, nt, num_rounds, x_obs):
    cm = cm.tocsc()
    x_vec = x_obs.toarray().astype(np.uint8).reshape(-1) if hasattr(x_obs, 'toarray') else np.asarray(x_obs, dtype=np.uint8).reshape(-1)
    mech_to_round = {}
    for m in range(cm.shape[1]):
        if m >= len(x_vec) or not x_vec[m]:
            continue
        col = cm[:, m].toarray().flatten()
        nonzero = np.where(col > 0)[0]
        if len(nonzero) == 0:
            continue
        r = int(nonzero[0]) // nt
        mech_to_round[m] = min(r, num_rounds - 1)
    decoder._mech_x_to_round = mech_to_round


def _find_affected_qubit_offset(col, num_rounds, num_cats, nqpc):
    """Given a standalone control syndrome column, return the data qubit
    offset (within n_data) for X/Y errors. Returns None if it's a Z error,
    measurement error, or unidentifiable."""
    per_round = len(col) // num_rounds
    n_z = num_cats * (nqpc - 1)  # Z generators per round
    z_dets = np.where(col[:num_rounds * per_round])[0]
    if len(z_dets) == 0:
        return None
    g = z_dets[0] % per_round
    if g >= n_z:
        return None  # X generator, Z error
    # Check if this is a measurement error (same gen fires in consecutive rounds)
    for zd in z_dets:
        if zd + per_round in z_dets and zd % per_round == (zd + per_round) % per_round:
            return None  # measurement error
    b = g // (nqpc - 1)
    z_dets_local = [z for z in z_dets if z % per_round == g or z % per_round == g + 1]
    if len(z_dets_local) > 1 and (z_dets_local[-1] % per_round) == g + 1:
        p = (g % (nqpc - 1)) + 1
    elif g % (nqpc - 1) == 0:
        p = 0
    else:
        p = nqpc - 1
    return b * nqpc + p


class StandaloneExactMwPartitionDecoder(Decoder):
    def __init__(self, target_code_utilities, control_code_utilities,
                 distance, modified_index, num_target_stabilizers, si=-1,
                 num_qubits_per_cat_state=None, target_decoder='mwpm'):
        self._target_code = target_code_utilities
        self._control_code = control_code_utilities
        self._distance = distance
        self._modified_index = modified_index
        self._num_target_stabs = num_target_stabilizers
        self._num_control_stabs = len(control_code_utilities.symplectic_matrix)
        self._num_rounds = distance + 1
        self._si = si
        self._num_active_blocks = si + 1  # number of cat blocks in the observable
        self._num_qubits_per_cat_state = num_qubits_per_cat_state if num_qubits_per_cat_state is not None else distance
        self._target_decoder = target_decoder

    def compile_decoder_for_dem(self, *, dem):
        from stim_experiments.simulate_cx.simulate_cx import SimulateCx

        combined_matrices = detector_error_model_to_check_matrices(
            dem, allow_undecomposed_hyperedges=True)
        combined_cm = combined_matrices.check_matrix.tocsc()
        combined_priors = list(combined_matrices.priors)
        combined_edge_cm = combined_matrices.edge_check_matrix.tocsc()
        combined_h2e = combined_matrices.hyperedge_to_edge_matrix
        combined_edge_obs = combined_matrices.edge_observables_matrix.toarray().astype(np.uint8)
        combined_obs = combined_matrices.observables_matrix
        p = _estimate_p(combined_priors)
        num_rounds = self._num_rounds
        nt = self._num_target_stabs
        nc = self._num_control_stabs
        num_gens = nt + nc
        num_combined_dets = dem.num_detectors
        has_cx = (self._modified_index is not None)

        # --- Build standalone TARGET decoder (pure single-code circuit) ---
        tgt_utils = _make_standalone_utils(self._target_code)
        tgt_circuit = SimulateCx.build_bare_circuit(
            tgt_utils, p, num_rounds, use_x_observable=False)
        tgt_dem = tgt_circuit.detector_error_model(decompose_errors=False)
        tgt_mats = detector_error_model_to_check_matrices(
            tgt_dem, allow_undecomposed_hyperedges=True)
        tgt_cm = tgt_mats.check_matrix.tocsc()
        tgt_obs = tgt_mats.observables_matrix
        tgt_priors = list(tgt_mats.priors)

        tgt_edge_cm = tgt_mats.edge_check_matrix.tocsc()
        tgt_h2e = tgt_mats.hyperedge_to_edge_matrix
        tgt_edge_obs = tgt_mats.edge_observables_matrix.toarray().astype(np.uint8)

        # X observable from combined DEM
        tgt_x_obs = None
        tgt_col_map = np.array([], dtype=int)
        if has_cx:
            is_target_per_round = np.zeros(num_combined_dets, dtype=bool)
            for r in range(num_rounds):
                is_target_per_round[r * num_gens:r * num_gens + nt] = True
            modified_mask = np.zeros(num_combined_dets, dtype=bool)
            for r in range(num_rounds):
                idx = r * num_gens + self._modified_index
                if idx < num_combined_dets:
                    modified_mask[idx] = True
            tgt_x_obs, tgt_col_map = _compute_x_obs_from_combined(
                combined_cm, is_target_per_round, modified_mask, tgt_cm, nt)
        else:
            tgt_x_obs = np.zeros((1, tgt_cm.shape[1]), dtype=np.uint8)

        tgt_decoder = self._build_target_decoder(
            tgt_cm, tgt_obs, tgt_priors, tgt_edge_cm, tgt_h2e, tgt_edge_obs,
            tgt_x_obs, nt, num_rounds)

        # --- Build CONTROL decoder from standalone circuit ---
        ctrl_circuit = SimulateCx.build_bare_circuit(
            self._control_code, p, num_rounds, use_x_observable=False)
        ctrl_dem = ctrl_circuit.detector_error_model(decompose_errors=False)
        ctrl_mats = detector_error_model_to_check_matrices(
            ctrl_dem, allow_undecomposed_hyperedges=True)
        ctrl_cm = ctrl_mats.check_matrix.tocsc()
        ctrl_obs = ctrl_mats.observables_matrix.toarray().astype(np.uint8)
        ctrl_priors = list(ctrl_mats.priors)

        # Restrict observable to first num_active_blocks subregisters.
        # The combined circuit's control observable is Z on the first qubit
        # of each active subregister (spaced by nqpc).
        nqpc = self._num_qubits_per_cat_state
        restricted_qubits = set(j * nqpc for j in range(self._num_active_blocks))
        ctrl_obs_arr = ctrl_obs.toarray().astype(np.uint8) if hasattr(ctrl_obs, 'toarray') else np.array(ctrl_obs, dtype=np.uint8)
        if self._num_active_blocks == 0:
            ctrl_obs_arr[:] = 0
        elif self._num_active_blocks < self._distance:
            for col_j in range(ctrl_cm.shape[1]):
                col = ctrl_cm[:, col_j].toarray().flatten()
                affected = _find_affected_qubit_offset(col.astype(np.uint8), num_rounds, self._distance, nqpc)
                if affected is not None:
                    ctrl_obs_arr[0, col_j] = 1 if affected in restricted_qubits else 0
        # else: full observable (all blocks), leave unchanged
        ctrl_obs = ctrl_obs_arr

        ctrl_edge_cm = ctrl_mats.edge_check_matrix.tocsc()
        ctrl_h2e = ctrl_mats.hyperedge_to_edge_matrix
        ctrl_edge_obs = ctrl_mats.edge_observables_matrix.toarray().astype(np.uint8)

        # Propagate column-level restriction to edge-level observable
        if self._num_active_blocks < self._distance:
            h2e_dense = ctrl_h2e.tocsc().toarray().astype(np.uint8)
            ctrl_edge_obs = (ctrl_obs @ h2e_dense.T) % 2

        ctrl_matcher, ctrl_edge_map, _ = _build_matcher(
            ctrl_edge_cm, ctrl_h2e, ctrl_priors,
            np.ones(ctrl_cm.shape[0], dtype=bool))
        ctrl_edge_obs_sub = (ctrl_edge_obs[:, ctrl_edge_map]
                             if ctrl_matcher is not None else np.array([]))

        ctrl_decoder = MwpmDecoder(
            ctrl_matcher, ctrl_edge_obs_sub, n_det=ctrl_cm.shape[0])

        # --- Modified detector indices within control-only syndrome ---
        modified_det_indices = np.array([], dtype=int)
        if has_cx:
            ctrl_mod_offset = self._modified_index - nt
            modified_det_indices = np.array([
                r * nc + ctrl_mod_offset
                for r in range(num_rounds)
            ], dtype=int)

        # --- Build extraction mask for target detectors ---
        n_tgt_final = tgt_cm.shape[0] - num_rounds * nt
        is_target_mask = np.zeros(num_combined_dets, dtype=bool)
        idx = 0
        for r in range(num_rounds):
            is_target_mask[idx:idx + nt] = True
            idx += num_gens
        if n_tgt_final > 0:
            is_target_mask[idx:idx + n_tgt_final] = True

        return CompiledStandaloneExactMwPartitionDecoder(
            tgt_decoder=tgt_decoder,
            ctrl_decoder=ctrl_decoder,
            num_detectors=num_combined_dets,
            is_target=is_target_mask,
            has_cx=has_cx,
            modified_det_indices=modified_det_indices,
            num_rounds=num_rounds,
            full_cm=combined_cm,
            tgt_col_map=tgt_col_map,
            is_target_per_round=is_target_per_round if has_cx else None,
        )

    def _build_target_decoder(self, cm, obs, priors, edge_cm, h2e, edge_obs,
                              x_obs, nt, num_rounds):
        if self._target_decoder == 'single_error':
            decoder = SingleErrorLookupDecoder(cm, obs, priors, x_obs=x_obs)
            if x_obs is not None:
                _setup_mech_x_to_round(decoder, cm, nt, num_rounds, x_obs)
            return decoder

        if self._target_decoder == 'bposd':
            decoder = BpOsdDecoder(cm, obs, priors, x_obs=x_obs)
            if x_obs is not None:
                _setup_mech_x_to_round(decoder, cm, nt, num_rounds, x_obs)
            return decoder

        if self._target_decoder == 'lookup':
            decoder = LookupTableDecoder(
                cm, obs, priors, x_obs=x_obs,
                fallback=BpOsdDecoder(cm, obs, priors, x_obs=x_obs))
            if x_obs is not None:
                _setup_mech_x_to_round(decoder, cm, nt, num_rounds, x_obs)
            return decoder

        # default: minimum-weight perfect matching
        matcher, edge_map, _ = _build_matcher(
            edge_cm, h2e, priors, np.ones(cm.shape[0], dtype=bool))
        edge_obs_sub = (edge_obs[:, edge_map]
                        if matcher is not None else np.array([]))
        decoder = MwpmDecoder(
            matcher, edge_obs_sub, n_det=cm.shape[0])
        if matcher is not None and x_obs is not None:
            h2e_dense = h2e.tocsc().toarray().astype(np.uint8)
            edge_x_full = (x_obs.astype(np.uint8) @ h2e_dense.T) % 2
            decoder._edge_x_obs = edge_x_full[:, edge_map]
            _setup_edge_to_round(decoder, edge_cm, nt, num_rounds, edge_map)
        return decoder


class CompiledStandaloneExactMwPartitionDecoder(CompiledDecoder):
    def __init__(self, tgt_decoder, ctrl_decoder,
                 num_detectors, is_target, has_cx, modified_det_indices,
                 num_rounds, full_cm=None, tgt_col_map=None,
                 is_target_per_round=None):
        self._tgt_decoder = tgt_decoder
        self._ctrl_decoder = ctrl_decoder
        self._num_detectors = num_detectors
        self._is_target = is_target
        self._has_cx = has_cx
        self._modified_det_indices = modified_det_indices
        self._num_rounds = num_rounds
        self._full_cm = full_cm
        self._tgt_col_map = tgt_col_map
        self._is_control_mask = ~is_target
        # For full_cm projection: control detector mask
        if has_cx and full_cm is not None and is_target_per_round is not None:
            # Control detectors include per-round control + non-target final dets
            self._ctrl_mask = np.zeros(full_cm.shape[0], dtype=bool)
            idx_ctrl = 0
            ngens = is_target_per_round.size // num_rounds  # maybe wrong, use is_control
            # Actually use is_control_mask
            self._ctrl_mask = ~is_target

    def decode_shots_bit_packed(self, *, bit_packed_detection_event_data):
        unpacked = np.unpackbits(
            bit_packed_detection_event_data, axis=1,
            bitorder='little'
        )[:, :self._num_detectors]
        num_shots = unpacked.shape[0]
        predictions = np.zeros((num_shots, 1), dtype=np.uint8)

        is_tgt = self._is_target
        not_tgt = ~is_tgt

        for i in range(num_shots):
            combined_syn = unpacked[i].astype(np.uint8)

            ts = combined_syn[is_tgt]
            cs = combined_syn[not_tgt].copy()

            if not ts.any() and not cs.any():
                continue

            tgt_pred, tgt_corr, tgt_x_pred = self._tgt_decoder.decode(ts)

            if self._has_cx:
                # Standalone correction has no combined effects; only
                # adjust the modified stabilizer, not the full projection.
                x_changes = self._tgt_decoder.get_x_changes(ts, self._num_rounds)
                for r in range(min(len(x_changes), len(self._modified_det_indices))):
                    if x_changes[r]:
                        mod_idx = self._modified_det_indices[r]
                        if mod_idx < len(cs):
                            cs[mod_idx] ^= 1

            ctrl_pred, _, _ = self._ctrl_decoder.decode(cs[:self._ctrl_decoder._n_det])
            predictions[i, 0] = tgt_pred ^ ctrl_pred

        return predictions
