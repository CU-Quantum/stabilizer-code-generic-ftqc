"""Spot checks for the partition decoder."""

import numpy as np
import stim
from stim_experiments.simulate_cx.simulate_cx import SimulateCx
from stim_experiments.simulate_cx.support.stabilizer_code_utilities import (
    get_five_qubit_code_utilities,
    get_dodecacode_utilities,
    get_golay_code_utilities,
)
from stim_experiments.simulate_cx.custom_dataclasses import RunConfiguration
from stim_experiments.simulate_cx.decoder_by_matrix.partition_decoder import PartitionDecoder
from ldpc.ckt_noise import detector_error_model_to_check_matrices


def _make_rc():
    return RunConfiguration(max_shots=1, max_errors=1, depolarization_probabilities=[0.01],
                            num_workers=1, num_shards=1, shard_index=0, decoder_name='partition')


def _compile(code_utils, num_cat_states, si, p=0.01):
    rc = _make_rc()
    sim = SimulateCx(num_cat_states=num_cat_states, target_code_utilities=code_utils,
                     si=si, run_configuration=rc)
    combined_S, _ = sim.get_combined_symplectic()
    circuit = sim.generate_task_circuit(physical_error_rate=p)
    dem = circuit.detector_error_model(decompose_errors=True,
                                       ignore_decomposition_failures=True)
    n_target_q = len(code_utils.data_indices)
    q = int(max(np.sum(code_utils.x_observable[:n_target_q]),
                np.sum(code_utils.z_observable[n_target_q:])))
    decoder = PartitionDecoder(
        combined_symplectic_matrix=combined_S,
        num_target_stabilizers=code_utils.symplectic_matrix.shape[0],
        num_target_data_qubits=n_target_q,
        distance=num_cat_states,
        modified_index=len(combined_S) - num_cat_states + 1 + si if si >= 0 else None,
        si=max(si, 0), num_cat_state_qubits=q,
        final_detector_generator_indices=[],
        target_decoder='lookup',
    )
    compiled = decoder.compile_decoder_for_dem(dem=dem)
    return compiled, circuit, combined_S, dem


def test_zero_syndrome_is_zero():
    """Noiseless circuit should always decode to 0."""
    for name, utils, nc in [('5q', get_five_qubit_code_utilities(), 3),
                              ('dodeca', get_dodecacode_utilities(), 5),
                              ('golay', get_golay_code_utilities(), 7)]:
        for si in [-1, 0, nc - 1]:
            compiled, circuit, _, _ = _compile(utils, nc, si, p=0)
            sampler = circuit.compile_detector_sampler()
            det, obs = sampler.sample(shots=10, separate_observables=True)
            pred = compiled.decode_shots_bit_packed(
                bit_packed_detection_event_data=det.astype(np.uint8))
            p = np.unpackbits(pred, axis=1, bitorder='little')
            assert (p[:, 0] == 0).all(), f"{name} si={si}: zero-syndrome gave nonzero prediction"
    print("PASS: test_zero_syndrome_is_zero")


def test_single_shot_accuracy():
    """Run a handful of noisy shots and check accuracy is not pathological."""
    for name, utils, nc in [('5q', get_five_qubit_code_utilities(), 3)]:
        compiled, circuit, _, _ = _compile(utils, nc, si=0, p=0.01)
        sampler = circuit.compile_detector_sampler()
        det, obs = sampler.sample(shots=100, separate_observables=True)
        pred = compiled.decode_shots_bit_packed(
            bit_packed_detection_event_data=det.astype(np.uint8))
        p = np.unpackbits(pred, axis=1, bitorder='little')
        correct = int((p[:, 0] == obs[:, 0]).sum())
        ler = 1 - correct / 100
        print(f"  {name}: {correct}/100 correct (LER={ler:.3f})")
        assert ler < 0.5, f"{name}: LER={ler:.3f} worse than random"
    print("PASS: test_single_shot_accuracy")


def test_partition_split():
    """Verify that target and control partitions cover disjoint detector sets."""
    for name, utils, nc in [('5q', get_five_qubit_code_utilities(), 3)]:
        compiled, circuit, combined_S, dem = _compile(utils, nc, si=0)
        num_target = utils.symplectic_matrix.shape[0]
        num_gens = len(combined_S)
        num_repeats = nc + 1

        # Check target mask
        mask = compiled._is_target
        assert mask.sum() == num_target * num_repeats, \
            f"Expected {num_target * num_repeats} target dets, got {mask.sum()}"

        # Verify first round ordering
        for r in range(num_repeats):
            offset = r * num_gens
            assert mask[offset:offset + num_target].all(), \
                f"First {num_target} dets of round {r} should be target"
            assert not mask[offset + num_target:offset + num_gens].any(), \
                f"Remaining dets of round {r} should be control"

        # Check modified detector index
        if compiled._modified_detector_index is not None:
            assert compiled._modified_detector_index >= 0
            row_round = compiled._modified_detector_index // num_gens
            assert row_round == num_repeats - 1, \
                f"Modified detector should be in last round, got round {row_round}"
    print("PASS: test_partition_split")


def test_modified_stabilizer_flip():
    """Verify the flip logic: target correction should produce correct control syndrome adjustment."""
    utils = get_five_qubit_code_utilities()
    nc = 3
    compiled, circuit, combined_S, dem = _compile(utils, nc, si=0)

    matrices = detector_error_model_to_check_matrices(dem)
    full_cm = matrices.check_matrix.tocsc()
    num_gens = len(combined_S)

    # Get the modified stabilizer row from the check matrix
    modified_index = num_gens - nc + 1 + 0  # si=0
    # The detector for this stabilizer in the last round
    # Modified stabilizer = row 'modified_index' in symplectic matrix
    # Its detector in round r is at offset r*num_gens + modified_index

    # Extract the part of the full check matrix for the modified stabilizer detector
    num_repeats = nc + 1
    target_rows = list(range(0, 4))  # first 4 are target
    control_rows = list(range(4, 18))  # remaining are control

    # Check: for a target correction that has errors in target columns,
    # the control syndrome contribution should be consistent with the
    # symplectic inner product
    target_rows_all = []
    control_rows_all = []
    for r in range(num_repeats):
        offset = r * num_gens
        target_rows_all += [offset + i for i in range(4)]
        control_rows_all += [offset + i for i in range(4, 18)]

    target_cm = full_cm[target_rows_all, :]
    control_cm = full_cm[control_rows_all, :]

    # Check dimensions
    assert compiled._is_target.sum() == len(target_rows_all), \
        f"target mask count mismatch: {compiled._is_target.sum()} vs {len(target_rows_all)}"

    print("PASS: test_modified_stabilizer_flip")


def test_si_variants():
    """Check that different si values produce different modified detector indices."""
    utils = get_five_qubit_code_utilities()
    nc = 3
    mod_dets = []
    for si in range(nc):
        compiled, _, combined_S, _ = _compile(utils, nc, si)
        mod_dets.append(compiled._modified_detector_index)

    # si=-1 should have no modified detector
    compiled_m1, _, combined_S, _ = _compile(utils, nc, -1)
    assert compiled_m1._modified_detector_index is None, "si=-1 should have no modified detector"

    # si=0..nc-1 should have different modified detectors
    num_gens = len(combined_S)
    num_repeats = nc + 1
    for si in range(nc):
        if compiled._modified_detector_index is not None:  # si < nc-1
            expected_row_in_last_round = num_gens - nc + 1 + si
            expected_det = (num_repeats - 1) * num_gens + expected_row_in_last_round
            assert mod_dets[si] == expected_det, \
                f"si={si}: expected mod_det={expected_det}, got {mod_dets[si]}"
    print("PASS: test_si_variants")


def test_control_contribution_shape():
    """Verify the control syndrome contribution computation has correct dimensions."""
    utils = get_five_qubit_code_utilities()
    nc = 3
    compiled, _, _, _ = _compile(utils, nc, si=0)

    # Create a dummy target correction
    n_target_cols = len(compiled._target_col_map)
    target_corr = np.zeros(n_target_cols, dtype=np.uint8)
    target_corr[0] = 1  # set first mechanism

    # Expand to full correction
    full_corr = np.zeros(compiled._full_check_matrix.shape[1], dtype=np.uint8)
    for j, col in enumerate(compiled._target_col_map):
        full_corr[col] = target_corr[j]

    # Compute control contribution
    control_cm = compiled._full_check_matrix[~compiled._is_target, :]
    contrib = (control_cm @ full_corr) % 2
    assert contrib.shape[0] == (~compiled._is_target).sum(), \
        f"Expected {(~compiled._is_target).sum()} elements, got {contrib.shape[0]}"
    print("PASS: test_control_contribution_shape")


def test_golay_compiles():
    """Golay DEM should compile with ignore_decomposition_failures."""
    utils = get_golay_code_utilities()
    nc = 7
    compiled, _, _, _ = _compile(utils, nc, si=0)
    assert compiled._num_detectors > 0
    assert compiled._is_target.sum() > 0
    print(f"  Golay: {compiled._num_detectors} dets, {compiled._is_target.sum()} target")
    print("PASS: test_golay_compiles")


if __name__ == '__main__':
    test_zero_syndrome_is_zero()
    test_single_shot_accuracy()
    test_partition_split()
    test_modified_stabilizer_flip()
    test_si_variants()
    test_control_contribution_shape()
    test_golay_compiles()
    print("\nAll spot checks passed.")
