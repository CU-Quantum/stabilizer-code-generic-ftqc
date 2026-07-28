"""Test: DEM-based partition split with union correction."""
import numpy as np
from ldpc.bposd_decoder import BpOsdDecoder
from ldpc.ckt_noise import detector_error_model_to_check_matrices
from sinter import CompiledDecoder

from stim_experiments.simulate_cx.simulate_cx import SimulateCx
from stim_experiments.simulate_cx.support.stabilizer_code_utilities import get_five_qubit_code_utilities
from stim_experiments.simulate_cx.custom_dataclasses import RunConfiguration
from stim_experiments.simulate_cx.decoder_by_matrix.bposd_decoder import BpOsdDecoderForSinter


def _filter_rows_cols(cm, row_mask):
    rows = np.where(row_mask)[0]
    sub = cm[rows, :]
    nz = np.diff(sub.indptr) > 0
    col_map = list(np.where(nz)[0])
    return sub[:, col_map].tocsc(), col_map


def test_dem_split():
    rc = RunConfiguration(max_shots=1, max_errors=1, depolarization_probabilities=[0.01],
                          num_workers=1, num_shards=1, shard_index=0, decoder_name='partition')
    utils = get_five_qubit_code_utilities()

    for si in [-1, 0]:
        sim = SimulateCx(num_cat_states=3, target_code_utilities=utils, si=si, run_configuration=rc)
        S, _ = sim.get_combined_symplectic()
        circuit = sim.generate_task_circuit(0.01)
        dem = circuit.detector_error_model(decompose_errors=True, ignore_decomposition_failures=True)

        matrices = detector_error_model_to_check_matrices(dem, allow_undecomposed_hyperedges=True)
        cm = matrices.check_matrix.tocsc()
        obs = matrices.observables_matrix.toarray().astype(np.uint8)
        priors = list(matrices.priors)

        num_target = utils.symplectic_matrix.shape[0]
        num_gens = S.shape[0]
        num_repeats = 4
        is_target = np.zeros(dem.num_detectors, dtype=bool)
        for r in range(num_repeats):
            is_target[r * num_gens:(r * num_gens) + num_target] = True

        # Target BP-OSD
        tgt_cm, tgt_map = _filter_rows_cols(cm, is_target)
        tgt_priors = [priors[c] for c in tgt_map]
        tgt_bposd = BpOsdDecoder(
            tgt_cm, error_channel=tgt_priors,
            max_iter=100, bp_method='ms', ms_scaling_factor=0.625,
            schedule='parallel', osd_method='osd_cs', osd_order=10,
        )

        # Control BP-OSD
        ctrl_cm, ctrl_map = _filter_rows_cols(cm, ~is_target)
        ctrl_priors = [priors[c] for c in ctrl_map]
        ctrl_bposd = BpOsdDecoder(
            ctrl_cm, error_channel=ctrl_priors,
            max_iter=100, bp_method='ms', ms_scaling_factor=0.625,
            schedule='parallel', osd_method='osd_cs', osd_order=10,
        )

        # Modified detector for flip
        mod_det = None
        if si >= 0:
            mod_index = num_gens - 3 + 1 + si
            if mod_index < num_gens:
                mod_det = (num_repeats - 1) * num_gens + mod_index

        collator = _Collator(cm, obs, tgt_map, ctrl_map, tgt_bposd, ctrl_bposd,
                             is_target, mod_det)
        return collator


class _Collator:
    def __init__(self, cm, obs, tgt_map, ctrl_map, tgt_bposd, ctrl_bposd,
                 is_target, mod_det):
        self.cm = cm
        self.obs = obs
        self.tgt_map = tgt_map
        self.ctrl_map = ctrl_map
        self.tgt_bposd = tgt_bposd
        self.ctrl_bposd = ctrl_bposd
        self.is_target = is_target
        self.mod_det = mod_det

    def decode(self, td, cd):
        # Step 1: target
        tgt_corr = self.tgt_bposd.decode(td) if td.any() else None

        # Step 2: subtract target contribution from control syndrome
        if tgt_corr is not None and self.mod_det is not None:
            full = np.zeros(self.cm.shape[1], dtype=np.uint8)
            for j, col in enumerate(self.tgt_map):
                full[col] = tgt_corr[j]
            contrib = (self.cm[~self.is_target, :] @ full) % 2
            cd = (cd ^ contrib.astype(np.uint8))

        # Step 3: control
        ctrl_corr = self.ctrl_bposd.decode(cd) if cd.any() else None

        # Step 4: union + observable
        full = np.zeros(self.cm.shape[1], dtype=np.uint8)
        if tgt_corr is not None:
            for j, col in enumerate(self.tgt_map):
                full[col] |= tgt_corr[j]
        if ctrl_corr is not None:
            for j, col in enumerate(self.ctrl_map):
                full[col] |= ctrl_corr[j]
        return int(((self.obs @ full) % 2)[0])


if __name__ == '__main__':
    rc = RunConfiguration(max_shots=1, max_errors=1, depolarization_probabilities=[0.01],
                          num_workers=1, num_shards=1, shard_index=0, decoder_name='partition')
    utils = get_five_qubit_code_utilities()

    for si in [-1, 0]:
        sim = SimulateCx(num_cat_states=3, target_code_utilities=utils, si=si, run_configuration=rc)
        S, _ = sim.get_combined_symplectic()
        circuit = sim.generate_task_circuit(0.01)
        dem = circuit.detector_error_model(decompose_errors=True, ignore_decomposition_failures=True)

        matrices = detector_error_model_to_check_matrices(dem, allow_undecomposed_hyperedges=True)
        cm = matrices.check_matrix.tocsc()
        obs = matrices.observables_matrix.toarray().astype(np.uint8)
        priors = list(matrices.priors)

        num_target = utils.symplectic_matrix.shape[0]
        num_gens = S.shape[0]
        num_repeats = 4
        is_target = np.zeros(dem.num_detectors, dtype=bool)
        for r in range(num_repeats):
            is_target[r * num_gens:(r * num_gens) + num_target] = True

        tgt_cm, tgt_map = _filter_rows_cols(cm, is_target)
        tgt_priors = [priors[c] for c in tgt_map]
        tgt_bposd = BpOsdDecoder(tgt_cm, error_channel=tgt_priors,
            max_iter=100, bp_method='ms', ms_scaling_factor=0.625,
            schedule='parallel', osd_method='osd_cs', osd_order=10)

        ctrl_cm, ctrl_map = _filter_rows_cols(cm, ~is_target)
        ctrl_priors = [priors[c] for c in ctrl_map]
        ctrl_bposd = BpOsdDecoder(ctrl_cm, error_channel=ctrl_priors,
            max_iter=100, bp_method='ms', ms_scaling_factor=0.625,
            schedule='parallel', osd_method='osd_cs', osd_order=10)

        mod_det = None
        if si >= 0:
            mi = num_gens - 3 + 1 + si
            if mi < num_gens:
                mod_det = (num_repeats - 1) * num_gens + mi

        collator = _Collator(cm, obs, tgt_map, ctrl_map, tgt_bposd, ctrl_bposd,
                             is_target, mod_det)

        # Compare against full DEM bposd
        full_dem = BpOsdDecoderForSinter().compile_decoder_for_dem(dem=dem)

        sampler = circuit.compile_detector_sampler()
        det, obs_vec = sampler.sample(shots=500, separate_observables=True)
        det_p = np.packbits(det.astype(np.uint8), axis=1, bitorder='little')
        det_u = np.unpackbits(det_p, axis=1, bitorder='little')[:, :dem.num_detectors]
        full_pred = np.unpackbits(
            full_dem.decode_shots_bit_packed(bit_packed_detection_event_data=det_p),
            axis=1, bitorder='little')

        correct = 0
        agree = 0
        for i in range(500):
            td_raw = det_u[i, is_target].astype(np.uint8)
            cd_raw = det_u[i, ~is_target].astype(np.uint8)
            p = collator.decode(td_raw, cd_raw)
            if p == obs_vec[i, 0]:
                correct += 1
            if p == full_pred[i, 0]:
                agree += 1

        print(f'si={si}: partition={correct}/500 ({100*correct/500:.1f}%), agree={agree}/500')
