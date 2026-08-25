"""Verify Golay code's logical gates and error correction."""
import numpy as np
from cirq import Circuit, LineQubit, X, Y, Z, I

from cirq_experiments.custom_dataclasses.logical_operation import LogicalGateLabel, LogicalOperation
from cirq_experiments.error_correcting_codes.stabilizer_standardized_code.stabilizer_standardized_code import \
    StabilizerStandardizedCode
from cirq_experiments.globals.fresh_ancillas_pool import FreshAncillasPool
from cirq_experiments.simulations.error_correcting_simulator import get_error_correcting_simulator
from cirq_experiments.utilities.utilities import KET_ONE_STATE_VECTOR, KET_ZERO_STATE_VECTOR, tensor, states_are_equal
from predefined_check_matrix_values import get_check_matrix_values_golay
from tests.cirq_experiments.utilities_for_tests import set_configuration_to_reduce_ancilla_qubits

set_configuration_to_reduce_ancilla_qubits()
generators = get_check_matrix_values_golay(balanced=True)
code = StabilizerStandardizedCode(generators=generators)
num_data_qubits = len(code.data_qubits)
FreshAncillasPool().set_first_ancilla_num(first_ancilla_num=num_data_qubits)

init_zero = tensor(*[KET_ZERO_STATE_VECTOR] * num_data_qubits)
encoding = code.encode_logical_qubit()
utilities = get_error_correcting_simulator(state=init_zero)

zero_L = utilities.run_simulation(
    circuit=encoding,
    num_data_qubits=num_data_qubits,
    initial_data_state=init_zero,
).state

init_one = tensor(*[KET_ZERO_STATE_VECTOR] * (num_data_qubits - 1), KET_ONE_STATE_VECTOR)
one_L = utilities.run_simulation(
    circuit=encoding,
    num_data_qubits=num_data_qubits,
    initial_data_state=init_one,
).state

print("=== Logical State Encoding ===")
print(f"  Zero state norm: {np.linalg.norm(zero_L):.6f}")
print(f"  One state norm: {np.linalg.norm(one_L):.6f}")
print(f"  <0_L|1_L>: {np.abs(np.vdot(zero_L, one_L)):.6e}")

print("\n=== Logical X Gate ===")
fresh = FreshAncillasPool()
fresh.set_first_ancilla_num(first_ancilla_num=num_data_qubits)
x_circuit = code.get_operation_circuit(LogicalOperation(gate=LogicalGateLabel.X, qubit_index=0))
x_result = utilities.run_simulation(
    circuit=Circuit([I(q) for q in code.data_qubits], x_circuit),
    num_data_qubits=num_data_qubits,
    initial_data_state=zero_L,
).state
print(f"  Are X|0_L> and |1_L> equal? {states_are_equal(x_result, one_L)}")

print("\n=== Logical Z Gate ===")
plus_L = (1/np.sqrt(2)) * (zero_L + one_L)
expected_minus_L = (1/np.sqrt(2)) * (zero_L - one_L)
fresh = FreshAncillasPool()
fresh.set_first_ancilla_num(first_ancilla_num=num_data_qubits)
z_circuit = code.get_operation_circuit(LogicalOperation(gate=LogicalGateLabel.Z, qubit_index=0))
z_result = utilities.run_simulation(
    circuit=Circuit([I(q) for q in code.data_qubits], z_circuit),
    num_data_qubits=num_data_qubits,
    initial_data_state=plus_L,
).state
print(f"  Are Z|+_L> and |-_L> equal? {states_are_equal(z_result, expected_minus_L)}")

print("\n=== Error Correction ===")
# Test X, Y, Z errors on various qubits
correction_circuit = code.get_error_correction_circuit().full_circuit
for gate_name, gate in [("X", X), ("Y", Y), ("Z", Z)]:
    for qi in [0, 11, 22]:
        fresh = FreshAncillasPool()
        fresh.set_first_ancilla_num(first_ancilla_num=num_data_qubits)
        sim = utilities.run_simulation(
            circuit=Circuit(gate(LineQubit(qi)), correction_circuit),
            num_data_qubits=num_data_qubits,
            initial_data_state=zero_L,
        ).state
        ok = states_are_equal(sim, zero_L)
        print(f"  {gate_name} on q{qi}: {'PASS' if ok else 'FAIL'}")
