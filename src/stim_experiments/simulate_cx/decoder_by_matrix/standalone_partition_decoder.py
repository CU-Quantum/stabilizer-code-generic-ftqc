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
    _filter_rows_cols, _build_matcher, _ExactMwDecoder,
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


class StandaloneExactMwPartitionDecoder(Decoder):
    def __init__(self, target_code_utilities, control_code_utilities,
                 distance, modified_index, num_target_stabilizers):
        self._target_code = target_code_utilities
        self._control_code = control_code_utilities
        self._distance = distance
        self._modified_index = modified_index
        self._num_target_stabs = num_target_stabilizers
        self._num_control_stabs = len(control_code_utilities.symplectic_matrix)
        self._num_rounds = distance + 1

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

        tgt_matcher, tgt_edge_map, _ = _build_matcher(
            tgt_edge_cm, tgt_h2e, tgt_priors, np.ones(tgt_cm.shape[0], dtype=bool))
        tgt_edge_obs_sub = (tgt_edge_obs[:, tgt_edge_map]
                            if tgt_matcher is not None else np.array([]))

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

        tgt_decoder = _ExactMwDecoder(
            tgt_cm, tgt_obs, tgt_priors, tgt_matcher, tgt_edge_obs_sub,
            x_obs=tgt_x_obs)

        if has_cx and tgt_matcher is not None and tgt_x_obs is not None:
            h2e_dense = tgt_h2e.tocsc().toarray().astype(np.uint8)
            edge_x_full = (tgt_x_obs.astype(np.uint8) @ h2e_dense.T) % 2
            tgt_decoder._edge_x_obs = edge_x_full[:, tgt_edge_map]
            _setup_edge_to_round(tgt_decoder, tgt_edge_cm, nt, num_rounds, tgt_edge_map)

        # --- Build CONTROL decoder from combined DEM partition ---
        # We use the combined DEM partition (not a standalone circuit) for the
        # control decoder because the combined circuit's control observable
        # includes only the first (si+1) cat blocks, not the full observable.
        is_control_mask = np.zeros(num_combined_dets, dtype=bool)
        idx = 0
        for r in range(num_rounds):
            is_control_mask[idx + nt:idx + num_gens] = True
            idx += num_gens
        n_tgt_final = tgt_cm.shape[0] - num_rounds * nt
        is_control_mask[idx + n_tgt_final:num_combined_dets] = True

        ctrl_cm, ctrl_map = _filter_rows_cols(combined_cm, is_control_mask)
        ctrl_priors = [combined_priors[c] for c in ctrl_map]
        ctrl_obs = combined_obs[:, ctrl_map] if combined_obs.shape[1] > 0 else np.array([[]])

        ctrl_matcher, ctrl_edge_map, _ = _build_matcher(
            combined_edge_cm, combined_h2e, combined_priors, is_control_mask)
        ctrl_edge_obs_sub = (combined_edge_obs[:, ctrl_edge_map]
                             if ctrl_matcher is not None else np.array([]))

        ctrl_decoder = _ExactMwDecoder(
            ctrl_cm, ctrl_obs, ctrl_priors, ctrl_matcher, ctrl_edge_obs_sub)

        # --- Modified detector indices within control-only syndrome ---
        modified_det_indices = np.array([], dtype=int)
        if has_cx:
            n_ctrl = ctrl_cm.shape[0] // num_rounds
            ctrl_mod_offset = self._modified_index - nt
            modified_det_indices = np.array([
                r * n_ctrl + ctrl_mod_offset
                for r in range(num_rounds)
            ], dtype=int)

        # --- Build extraction mask for target detectors ---
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
                if tgt_corr is not None and self._full_cm is not None and len(self._tgt_col_map) > 0:
                    full_c = np.zeros(self._full_cm.shape[1], dtype=np.uint8)
                    for j in range(min(len(tgt_corr), len(self._tgt_col_map))):
                        col = self._tgt_col_map[j]
                        if col >= 0 and tgt_corr[j]:
                            full_c[col] = 1
                    contrib = (self._full_cm[not_tgt, :] @ full_c) % 2
                    cs ^= contrib.astype(np.uint8)
                else:
                    x_changes = self._tgt_decoder.get_x_changes(ts, self._num_rounds)
                    for r in range(min(len(x_changes), len(self._modified_det_indices))):
                        if x_changes[r]:
                            mod_idx = self._modified_det_indices[r]
                            if mod_idx < len(cs):
                                cs[mod_idx] ^= 1

            ctrl_pred, _, _ = self._ctrl_decoder.decode(cs)
            predictions[i, 0] = tgt_pred ^ ctrl_pred

        return predictions
