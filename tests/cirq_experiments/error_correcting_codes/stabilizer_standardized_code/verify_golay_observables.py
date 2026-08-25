"""Verify Golay code observables in the stim utilities."""
import numpy as np
from predefined_check_matrix_values import get_check_matrix_values_golay

def get_golay_code_utilities(balanced=True):
    symplectic_matrix = get_check_matrix_values_golay(balanced=balanced)
    n_qubits = symplectic_matrix.shape[1] // 2
    n_stabilizers = symplectic_matrix.shape[0]
    r = n_stabilizers // 2
    H = symplectic_matrix[:r, :n_qubits].astype(np.uint8)

    x_obs_part = np.array([1, 0, 1, 0, 1, 1, 1, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=int)
    z_obs_part = np.array([1, 1, 0, 1, 0, 0, 1, 0, 1, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=int)
    observable_x = np.concatenate([x_obs_part, np.zeros(n_qubits, dtype=int)])
    observable_z = np.concatenate([np.zeros(n_qubits, dtype=int), z_obs_part])

    return symplectic_matrix, observable_x, observable_z

S, ox, oz = get_golay_code_utilities(balanced=True)
n = S.shape[1] // 2

# Verify observables:
# 1. X obs must commute with all stabilizers: symplectic inner product = 0
# Symplectic inner product: ox @ Omega @ S^T (mod 2)
Omega = np.block([[np.zeros((n, n)), np.eye(n, dtype=int)],
                  [np.eye(n, dtype=int), np.zeros((n, n))]])
ox_valid = all(((S @ Omega @ ox) % 2).flatten() == 0)
oz_valid = all(((S @ Omega @ oz) % 2).flatten() == 0)
print(f"X observable commutes with all stabilizers: {ox_valid}")
print(f"Z observable commutes with all stabilizers: {oz_valid}")

# 2. X and Z must anti-commute
anti = (ox @ Omega @ oz) % 2
print(f"X and Z anti-commute: {anti == 1}")

# 3. Weights
print(f"X weight: {np.count_nonzero(ox)}")
print(f"Z weight: {np.count_nonzero(oz)}")

# 4. Check if there are lower-weight logical operators
# Find all vectors v such that S @ Omega @ v = 0 (mod 2)
# This is the nullspace of S @ Omega
M = (S @ Omega) % 2
from scipy.linalg import null_space
ns = null_space(M.astype(float))
ns = (ns / ns[0, 0]).astype(int) % 2  # Normalize and mod 2
print(f"\nNullspace dimension: {ns.shape[1]}")
for i in range(min(5, ns.shape[1])):
    v = ns[:, i] % 2
    wt = np.count_nonzero(v)
    print(f"  Nullspace vector {i}: weight={wt}")
