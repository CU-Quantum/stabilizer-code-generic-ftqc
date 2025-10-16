"""
Shor's 9-qubit code: one error correction round in Stim with simple recoveries.

We construct a single round that measures the 8 stabilizer generators using MPP:
- Bit-flip checks (Z-pair parities in each 3-qubit block):
  S0 = Z0*Z1, S1 = Z1*Z2, S2 = Z3*Z4, S3 = Z4*Z5, S4 = Z6*Z7, S5 = Z7*Z8
- Phase-flip checks (X across neighboring blocks):
  S6 = X0*X1*X2*X3*X4*X5, S7 = X3*X4*X5*X6*X7*X8

Decoding/recovery:
- X corrections (bit-flip): for each block j in {0,1,2}, use its two Z-parity syndromes
  (s_a, s_b) to choose which qubit to flip using mapping
    (0,0)-> none, (1,0)-> first, (1,1)-> middle, (0,1)-> last
- Z corrections (phase-flip): use the two cross-block X syndromes (t0, t1) with mapping
    (0,0)-> none, (1,0)-> block0, (1,1)-> block1, (0,1)-> block2
  and apply a Z to the first qubit of the indicated block (representative correction).

We expose:
- build_shor_one_round_circuit(injected_error: Optional[Tuple[str,int]])
- decode_shor_syndrome(dets: np.ndarray) -> (x_corr: np.ndarray, z_corr: np.ndarray)
- run_shor_round_with_recovery(shots=1, injected_error=None)

The circuit uses only data qubits (0..8), direct parity measurements (MPP), and DETECTORs.
"""
from __future__ import annotations

from typing import Dict, List, Optional, Tuple

import numpy as np
import stim

# Data qubit indices and grouping for Shor code
DATA_QUBITS: List[int] = list(range(9))
BLOCKS: List[List[int]] = [
    [0, 1, 2],
    [3, 4, 5],
    [6, 7, 8],
]
# Stabilizer definition order (8 total)
Z_PAIR_CHECKS: List[Tuple[int, int]] = [
    (0, 1), (1, 2),
    (3, 4), (4, 5),
    (6, 7), (7, 8),
]
X_CROSS_CHECKS: List[List[int]] = [
    [0, 1, 2, 3, 4, 5],
    [3, 4, 5, 6, 7, 8],
]


def _mpp_line(paulis: List[Tuple[str, int]]) -> str:
    return "MPP " + "*".join(f"{p}{q}" for p, q in paulis)


def build_shor_one_round_circuit(injected_error: Optional[Tuple[str, int]] = None) -> stim.Circuit:
    """Build a Stim circuit measuring Shor code stabilizers once.

    Args:
        injected_error: Optional tuple (pauli, qubit) where pauli in {"X","Z"}
            is applied before the stabilizer measurements to simulate a single error.

    Returns:
        A stim.Circuit with 9 data qubits, 8 parity measurements, and 8 DETECTORs.
    """
    c = stim.Circuit()

    # Optional: label coordinates per qubit (not vital for logic)
    for q in DATA_QUBITS:
        c.append("QUBIT_COORDS", [q], [float(q % 3), float(q // 3)])

    # Inject a single Pauli error if requested (before measurements)
    if injected_error is not None:
        p, q = injected_error
        p = p.upper()
        if p == "X":
            c.append("X", [q])
        elif p == "Z":
            c.append("Z", [q])
        else:
            raise ValueError("injected_error pauli must be 'X' or 'Z'")

    # Measure Z pair checks (6 of them)
    for a, b in Z_PAIR_CHECKS:
        c += stim.Circuit(_mpp_line([("Z", a), ("Z", b)]) + "\n")
        # Add a detector referencing the most recent measurement
        c.append(stim.Detector(targets=[stim.target_rec(-1)]))

    # Measure X cross-block checks (2 of them)
    for group in X_CROSS_CHECKS:
        c += stim.Circuit(_mpp_line([("X", q) for q in group]) + "\n")
        c.append(stim.Detector(targets=[stim.target_rec(-1)]))

    return c


def decode_shor_syndrome(det_rows: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
    """Decode Shor one-round syndromes to per-qubit X and Z corrections.

    Args:
        det_rows: ndarray of shape (shots, 8) with the 8 detector bits ordered as
            [Z01, Z12, Z34, Z45, Z67, Z78, X012345, X345678].

    Returns:
        x_corr, z_corr: boolean ndarrays of shape (shots, 9). True indicates applying
        that Pauli correction to the corresponding qubit.
    """
    if det_rows.ndim != 2 or det_rows.shape[1] != 8:
        raise ValueError("det_rows must have shape (shots, 8)")
    shots = det_rows.shape[0]
    x_corr = np.zeros((shots, 9), dtype=bool)
    z_corr = np.zeros((shots, 9), dtype=bool)

    # Bit-flip corrections per block using two Z-pair checks
    # Block 0 uses det[0], det[1]; Block 1 uses det[2], det[3]; Block 2 uses det[4], det[5]
    z_pairs = det_rows[:, :6]
    for block_idx, start_det in enumerate([0, 2, 4]):
        s_a = z_pairs[:, start_det + 0]
        s_b = z_pairs[:, start_det + 1]
        q0, q1, q2 = BLOCKS[block_idx]
        # mapping
        x_corr[:, q0] |= (s_a & ~s_b)
        x_corr[:, q1] |= (s_a & s_b)
        x_corr[:, q2] |= (~s_a & s_b)

    # Phase-flip corrections using the two X cross-block checks
    t0 = det_rows[:, 6]
    t1 = det_rows[:, 7]
    # mapping to block index
    blk0 = t0 & ~t1
    blk1 = t0 & t1
    blk2 = ~t0 & t1
    # apply Z to first qubit of the chosen block as a representative correction
    z_corr[:, BLOCKS[0][0]] |= blk0
    z_corr[:, BLOCKS[1][0]] |= blk1
    z_corr[:, BLOCKS[2][0]] |= blk2

    return x_corr, z_corr


def _syndrome_from_paulis(x_ops: np.ndarray, z_ops: np.ndarray) -> np.ndarray:
    """Compute the 8-bit stabilizer syndrome for given per-qubit X/Z Paulis.

    Args:
        x_ops: boolean shape (9,) marking which qubits have an X component.
        z_ops: boolean shape (9,) marking which qubits have a Z component.

    Returns:
        Boolean array of shape (8,) with detector order
        [Z01, Z12, Z34, Z45, Z67, Z78, X012345, X345678].
    """
    if x_ops.shape != (9,) or z_ops.shape != (9,):
        raise ValueError("x_ops and z_ops must be shape (9,)")
    synd = np.zeros(8, dtype=bool)
    # Z pair checks flip if an odd number of Xs in the pair
    for i, (a, b) in enumerate(Z_PAIR_CHECKS):
        synd[i] = bool(x_ops[a] ^ x_ops[b])
    # X cross checks flip if an odd number of Zs in the group
    synd[6] = bool(np.bitwise_xor.reduce(z_ops[X_CROSS_CHECKS[0]]))
    synd[7] = bool(np.bitwise_xor.reduce(z_ops[X_CROSS_CHECKS[1]]))
    return synd


def run_shor_round_with_recovery(
    shots: int = 1,
    *,
    injected_error: Optional[Tuple[str, int]] = None,
    seed: Optional[int] = None,
) -> Dict[str, object]:
    """Run one Shor round, sample syndromes, and compute/apply recovery operations.

    In addition to returning the suggested X/Z corrections from the decoder,
    this function classically applies those corrections on top of any injected
    error and determines whether the final state matches the expected logical
    state (up to stabilizers), not merely whether the final syndrome is zero.

    We judge "final state matches expected" by checking that the residual Pauli
    after applying corrections performs no logical action: it commutes with both
    a chosen pair of logical operators for the Shor code.

    We use the following logicals:
      - X_L = X on all 9 data qubits.
      - Z_L = Z on qubits {0, 3, 6} (one per block).

    Args:
        shots: number of repetitions to sample.
        injected_error: optional ("X"|"Z", qubit) injected before measurements.
        seed: RNG seed forwarded to Stim's sampler.

    Returns:
        dict with keys: circuit, detections, x_corrections, z_corrections,
        final_syndrome, final_logical_flips, final_matches_expected
    """
    circuit = build_shor_one_round_circuit(injected_error=injected_error)
    det_sampler = circuit.compile_detector_sampler(seed=seed)
    dets = det_sampler.sample(shots=shots)

    x_corr, z_corr = decode_shor_syndrome(dets)

    # Build per-shot injected error vectors (x_err, z_err)
    if injected_error is None:
        x_err = np.zeros((shots, 9), dtype=bool)
        z_err = np.zeros((shots, 9), dtype=bool)
    else:
        p, q = injected_error
        p = p.upper()
        x_err = np.zeros((shots, 9), dtype=bool)
        z_err = np.zeros((shots, 9), dtype=bool)
        if p == "X":
            x_err[:, q] = True
        elif p == "Z":
            z_err[:, q] = True
        else:
            raise ValueError("injected_error pauli must be 'X' or 'Z'")

    # Apply corrections in the Pauli frame
    x_total = x_err ^ x_corr
    z_total = z_err ^ z_corr

    # Compute final syndromes after applying corrections (still useful to inspect)
    final_syndrome = np.zeros((shots, 8), dtype=bool)
    for s in range(shots):
        final_syndrome[s] = _syndrome_from_paulis(x_total[s], z_total[s])

    # Determine logical effect of the residual Pauli.
    # Z_L = Z on {0,3,6}: anticommutes with X on those positions -> logical Z flip
    zL_qubits = np.array([0, 3, 6], dtype=int)
    # X_L = X on all 9: anticommutes with any Z -> parity of Z across all qubits
    # Compute per-shot parities.
    logical_Z_flip = (x_total[:, zL_qubits].sum(axis=1) % 2 == 1)
    logical_X_flip = (z_total.sum(axis=1) % 2 == 1)
    final_logical_flips = np.stack([logical_Z_flip, logical_X_flip], axis=1)

    # Final state matches expected iff no logical flips occurred.
    final_matches_expected = ~(logical_Z_flip | logical_X_flip)

    return {
        "circuit": circuit,
        "detections": dets,
        "x_corrections": x_corr,
        "z_corrections": z_corr,
        "final_syndrome": final_syndrome,
        "final_logical_flips": final_logical_flips,
        "final_matches_expected": final_matches_expected,
    }


def main() -> None:
    import argparse

    parser = argparse.ArgumentParser(description="Stim Shor code: one EC round with simple recovery")
    parser.add_argument("--shots", type=int, default=1)
    parser.add_argument("--inject", type=str, default=None, help="e.g., X3 or Z7")
    parser.add_argument("--seed", type=int, default=None)
    args = parser.parse_args()

    injected = None
    if args.inject:
        if len(args.inject) < 2 or args.inject[0].upper() not in {"X", "Z"}:
            raise SystemExit("--inject should look like X3 or Z7")
        p = args.inject[0].upper()
        q = int(args.inject[1:])
        injected = (p, q)

    res = run_shor_round_with_recovery(shots=args.shots, injected_error=injected, seed=args.seed)

    print("Circuit (first 20 lines):")
    lines = str(res["circuit"]).splitlines()
    for line in lines[:20]:
        print(line)
    if len(lines) > 20:
        print("...")

    print("\nDetections:")
    print(res["detections"].astype(int))
    print("X corrections (True means apply X):")
    print(res["x_corrections"].astype(int))
    print("Z corrections (True means apply Z):")
    print(res["z_corrections"].astype(int))


if __name__ == "__main__":
    main()
