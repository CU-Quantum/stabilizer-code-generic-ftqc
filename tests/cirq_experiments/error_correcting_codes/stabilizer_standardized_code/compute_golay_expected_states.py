"""Compute and save expected logical states for the Golay [[23,1,7]] code using GolayCode."""
import pickle
from pathlib import Path

import numpy as np

from cirq_experiments.error_correcting_codes.golay_code.golay_code import GolayCode
from cirq_experiments.globals.fresh_ancillas_pool import FreshAncillasPool
from cirq_experiments.simulations.error_correcting_simulator import get_error_correcting_simulator
from cirq_experiments.utilities.utilities import KET_ONE_STATE_VECTOR, KET_ZERO_STATE_VECTOR, tensor
from tests.cirq_experiments.utilities_for_tests import set_configuration_to_reduce_ancilla_qubits

set_configuration_to_reduce_ancilla_qubits()
code = GolayCode()
num_data_qubits = len(code.data_qubits)
print(f"Data qubits: {num_data_qubits}")

FreshAncillasPool().set_first_ancilla_num(first_ancilla_num=num_data_qubits)
encoding = code.encode_logical_qubit()

init_zero = tensor(*[KET_ZERO_STATE_VECTOR] * num_data_qubits)
utilities = get_error_correcting_simulator(state=init_zero)
logical_zero = utilities.run_simulation(
    circuit=encoding,
    num_data_qubits=num_data_qubits,
    initial_data_state=init_zero,
).state

init_one = tensor(*[KET_ZERO_STATE_VECTOR] * (num_data_qubits - 1), KET_ONE_STATE_VECTOR)
utilities = get_error_correcting_simulator(state=init_one)
logical_one = utilities.run_simulation(
    circuit=encoding,
    num_data_qubits=num_data_qubits,
    initial_data_state=init_one,
).state

norm_zero = np.linalg.norm(logical_zero)
norm_one = np.linalg.norm(logical_one)
print(f"Logical zero norm: {norm_zero:.6f}")
print(f"Logical one norm: {norm_one:.6f}")
print(f"Logical zero nonzero entries: {np.count_nonzero(~np.isclose(logical_zero, 0))}")
print(f"Logical one nonzero entries: {np.count_nonzero(~np.isclose(logical_one, 0))}")
print(f"Inner product <0_L|1_L>: {np.abs(np.vdot(logical_zero, logical_one)):.6e}")

output_dir = Path(__file__).parent
with open(output_dir / 'golay_logical_zero.pkl', 'wb') as f:
    pickle.dump(logical_zero, f)
with open(output_dir / 'golay_logical_one.pkl', 'wb') as f:
    pickle.dump(logical_one, f)
print(f"Saved states to {output_dir}")
