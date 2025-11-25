"""
Use Stim's built-in generated surface code circuit to run a single round
of error detection for a rotated distance-3 code, and include recovery
operations (via decoding the detection events into a Pauli frame).

We build the circuit using:
    stim.Circuit.generated("surface_code:rotated_memory_x", rounds=1, distance=3, ...)

Then we:
- sample detection events from the circuit,
- extract a detector error model (DEM),
- build a decoder from the DEM (PyMatching if available),
- decode detection events to predict logical flips (the recovery / Pauli frame),
- compare to ground-truth logical flips sampled from the DEM to estimate
  pre- and post-recovery logical error rates.

If PyMatching is not installed, we still build and sample the circuit and
print a notice that recovery is skipped.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Any, Optional

import stim

try:
    from pymatching import Matching  # type: ignore
    _HAS_PYMATCHING = True
except Exception:  # pragma: no cover - optional dependency
    Matching = None  # type: ignore
    _HAS_PYMATCHING = False


@dataclass
class SurfaceCodeParams:
    # Noise parameters following Stim's generated circuit API names.
    after_clifford_depolarization: float = 0.0
    after_reset_flip_probability: float = 0.0
    before_measure_flip_probability: float = 0.0
    before_round_data_depolarization: float = 0.0
    # Code parameters
    distance: int = 3
    rounds: int = 1


def build_rotated_memory_x_circuit(params: SurfaceCodeParams) -> stim.Circuit:
    """Build a rotated surface code memory (X) circuit using Stim's generated API."""
    c = stim.Circuit.generated(
        "surface_code:rotated_memory_x",
        rounds=params.rounds,
        distance=params.distance,
        after_clifford_depolarization=params.after_clifford_depolarization,
        after_reset_flip_probability=params.after_reset_flip_probability,
        before_measure_flip_probability=params.before_measure_flip_probability,
        before_round_data_depolarization=params.before_round_data_depolarization,
    )
    return c


def run_single_round_with_recovery(
    shots: int = 1000,
    *,
    params: Optional[SurfaceCodeParams] = None,
    seed: Optional[int] = None,
) -> Dict[str, Any]:
    """
    Runs one round of rotated surface code error detection and performs recovery
    (decoding) when PyMatching is available.

    Returns a dict containing the circuit, raw detection events, predicted logical
    flips from the decoder (if available), ground-truth observable flips, and basic
    stats.
    """
    if params is None:
        params = SurfaceCodeParams()
    if params.rounds != 1:
        # Force one round per the issue requirement.
        params.rounds = 1

    circuit = build_rotated_memory_x_circuit(params)

    # Sample detection events from the circuit.
    det_sampler = circuit.compile_detector_sampler(seed=seed)
    det_data = det_sampler.sample(shots=shots)

    # Extract the detector error model and create a decoder.
    dem = circuit.detector_error_model(decompose_errors=True)

    # Get ground-truth observable flips from the detector error model's sampler.
    # This simulates the same noise model at the DEM level and returns
    # (det_data, obs_data, err_data) when return_errors=True.
    dem_sampler = dem.compile_sampler(seed=seed)
    det_data_dem, obs_data, _ = dem_sampler.sample(shots=shots, return_errors=True)

    # For sanity, the DEM dets should be consistent in shape with circuit dets.
    assert det_data.shape == det_data_dem.shape, (
        "Detector sample shape mismatch between circuit and DEM."
    )

    predicted_obs = None
    post_recovery_logical_error_rate = None

    if _HAS_PYMATCHING:
        pm = Matching.from_detector_error_model(dem)
        # Decode the detection events into predicted observable flips (Pauli frame updates).
        predicted_obs = pm.decode_batch(det_data)
        # Compute a post-recovery logical error rate by comparing predicted vs actual obs.
        # A logical error occurs when predicted != actual for any observable in the shot.
        diff = predicted_obs ^ obs_data
        # If there are multiple observables, consider an error when any differs.
        per_shot_error = diff.any(axis=1) if diff.ndim == 2 else diff
        post_recovery_logical_error_rate = per_shot_error.mean()

    # Pre-recovery logical error rate: just the fraction of shots where any observable flipped.
    pre_recovery_logical_error_rate = obs_data.any(axis=1).mean() if obs_data.ndim == 2 else obs_data.mean()

    return {
        "circuit": circuit,
        "detector_error_model": dem,
        "detections": det_data,  # shape (shots, num_detectors)
        "observables": obs_data,  # shape (shots, num_observables)
        "predicted_observables": predicted_obs,  # None if no decoder
        "pre_recovery_logical_error_rate": pre_recovery_logical_error_rate,
        "post_recovery_logical_error_rate": post_recovery_logical_error_rate,
        "decoder": "PyMatching" if _HAS_PYMATCHING else None,
    }


def main() -> None:
    import argparse
    import numpy as np

    parser = argparse.ArgumentParser(description="Single-round rotated surface code (X) with decoding")
    parser.add_argument("--shots", type=int, default=1000)
    parser.add_argument("--distance", type=int, default=3)
    parser.add_argument("--after_clifford", type=float, default=0.001, help="after_clifford_depolarization")
    parser.add_argument("--after_reset", type=float, default=0.001, help="after_reset_flip_probability")
    parser.add_argument("--before_measure", type=float, default=0.001, help="before_measure_flip_probability")
    parser.add_argument("--before_round", type=float, default=0.001, help="before_round_data_depolarization")
    parser.add_argument("--seed", type=int, default=None)
    args = parser.parse_args()

    params = SurfaceCodeParams(
        distance=args.distance,
        rounds=1,
        after_clifford_depolarization=args.after_clifford,
        after_reset_flip_probability=args.after_reset,
        before_measure_flip_probability=args.before_measure,
        before_round_data_depolarization=args.before_round,
    )

    result = run_single_round_with_recovery(shots=args.shots, params=params, seed=args.seed)

    circuit: stim.Circuit = result["circuit"]
    dem: stim.DetectorErrorModel = result["detector_error_model"]
    dets = result["detections"]
    obs = result["observables"]
    pred = result["predicted_observables"]

    print("Constructed Stim generated circuit (first 40 lines):")
    circ_lines = str(circuit).splitlines()
    for line in circ_lines[:40]:
        print(line)
    if len(circ_lines) > 40:
        print("...")

    print("\nCircuit summary:")
    print(f"- num qubits: {circuit.num_qubits}")
    print(f"- num detectors: {circuit.num_detectors}")
    print(f"- num observables: {circuit.num_observables}")

    print("\nSampling summary:")
    print(f"- shots: {args.shots}")
    print(f"- detections shape: {dets.shape}")
    print(f"- observables shape: {obs.shape}")

    # Basic detection event rates per detector.
    det_rates = dets.mean(axis=0) if dets.size else np.zeros((0,))
    print("- mean detection event rates (first 16):", det_rates[:16])

    pre = result["pre_recovery_logical_error_rate"]
    post = result["post_recovery_logical_error_rate"]
    decoder_name = result["decoder"]

    print("\nLogical error rates:")
    print(f"- pre-recovery:  {pre:.6f}")
    if decoder_name is None:
        print("- post-recovery: (decoder not available; install pymatching)")
    else:
        print(f"- post-recovery: {post:.6f} (decoder: {decoder_name})")
        # Also show how often decoder's prediction matches the ground truth.
        match_rate = 1.0 - (pred ^ obs).any(axis=1).mean()
        print(f"- decoder agreement rate: {match_rate:.6f}")

    # Show a small sample of detections and predictions.
    print("\nExample rows (up to 5 shots):")
    for i in range(min(5, args.shots)):
        det_row = dets[i].astype(int)
        obs_row = obs[i].astype(int)
        if pred is not None:
            pred_row = pred[i].astype(int)
            print(f"shot {i}: det={det_row} obs={obs_row} pred_obs={pred_row}")
        else:
            print(f"shot {i}: det={det_row} obs={obs_row}")


if __name__ == "__main__":
    main()
