import numpy as np

from stim_experiments.simulate_cx.custom_dataclasses import RunConfiguration
from stim_experiments.simulate_cx.simulate_cx import SimulateCx
from stim_experiments.simulate_cx.support.stabilizer_code_utilities import (
    get_five_qubit_code_utilities,
    get_gscx_code_utilities,
)


def _sample_ler(code_utils, num_cat_states, si, p, n_shots, seed=42):
    rc = RunConfiguration(max_shots=1, max_errors=1, depolarization_probabilities=[p],
                          num_workers=1, num_shards=1, shard_index=0)
    sim = SimulateCx(num_cat_states=num_cat_states, target_code_utilities=code_utils,
                     si=si, run_configuration=rc)
    circuit = sim.generate_task_circuit(p)
    dem = circuit.detector_error_model(decompose_errors=False)
    compiled = sim.build_decoder().compile_decoder_for_dem(dem=dem)
    sampler = circuit.compile_detector_sampler(seed=seed)
    det, obs = sampler.sample(shots=n_shots, separate_observables=True)
    packed = np.packbits(det.astype(np.uint8), axis=1, bitorder='little')
    pred = compiled.decode_shots_bit_packed(bit_packed_detection_event_data=packed)
    pv = np.unpackbits(pred, axis=1, bitorder='little')
    return float((pv[:n_shots, 0] != obs[:n_shots, 0]).mean())


def test_zero_syndrome_decodes_to_zero():
    for code_utils, num_cat_states in [
        (get_five_qubit_code_utilities(), 3),
        (get_gscx_code_utilities(distance=7), 7),
    ]:
        ler = _sample_ler(code_utils, num_cat_states, si=0, p=0.0, n_shots=10)
        assert ler == 0.0, f"{code_utils.code_name}: noiseless circuit gave LER {ler}"


def test_noisy_five_qubit_accuracy_bounded():
    ler = _sample_ler(get_five_qubit_code_utilities(), 3, si=0, p=0.01, n_shots=100)
    assert 0.0 <= ler < 0.05, f"five_qubit LER={ler} out of expected range"


def test_target_partition_mask_covers_per_round_target_detectors():
    rc = RunConfiguration(max_shots=1, max_errors=1, depolarization_probabilities=[0.0],
                          num_workers=1, num_shards=1, shard_index=0)
    utils = get_five_qubit_code_utilities()
    sim = SimulateCx(num_cat_states=3, target_code_utilities=utils, si=0, run_configuration=rc)
    circuit = sim.generate_task_circuit(0.0)
    dem = circuit.detector_error_model(decompose_errors=False)
    compiled = sim.build_decoder().compile_decoder_for_dem(dem=dem)

    num_target = len(utils.symplectic_matrix)
    num_rounds = sim._num_cat_states + 1
    mask = compiled._is_target
    assert mask[:num_target].all()
    assert int(mask.sum()) >= num_target * num_rounds
    assert (~mask).any()
