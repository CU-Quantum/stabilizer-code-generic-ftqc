import pytest
from cirq import Circuit, KET_ONE, KET_PLUS, KET_ZERO, Z, kron
from numpy import allclose

from stim_experiments.error_correcting_codes.generic_stabilizer_code.generic_stabilizer_code import \
    GenericStabilizerCode
from stim_experiments.custom_dataclasses.logical_operation import LogicalGateLabel, LogicalOperation
from stim_experiments.utilities import KET_ONE_DENSITY_MATRIX, KET_PLUS_DENSITY_MATRIX, KET_ZERO_DENSITY_MATRIX, tensor
from tests.error_correcting_codes.generic_stabilizer_code.expected_states_generic_5_qubit import \
    ExpectedStatesGenericFiveQubit
from tests.error_correcting_codes.generic_stabilizer_code.utilities import get_check_matrix_values_4_qubit, \
    get_check_matrix_values_5_qubit, get_check_matrix_values_8_qubit


class TestLogicalGates:
    def test_logical_x(self):
        operation = LogicalOperation(gate=LogicalGateLabel.X, qubit_index=0)
        code = GenericStabilizerCode(generators=get_check_matrix_values_5_qubit())
        state = code.encode_logical_qubit()
        circuit = Circuit(
            code.get_operation_circuit(operation=operation)
        )
        current_state = code.error_correcting_code_utilities.get_state_after_circuit(circuit=circuit,
                                                                                     qubit_order=code.all_qubits,
                                                                                     initial_state=state)
        expected_state = ExpectedStatesGenericFiveQubit().get_logical_one_state_vector()
        assert allclose(current_state.state, expected_state)

    def test_logical_z(self):
        operation = LogicalOperation(gate=LogicalGateLabel.Z, qubit_index=0)
        code = GenericStabilizerCode(generators=get_check_matrix_values_5_qubit(), initial_logical_qubit_state=KET_PLUS_DENSITY_MATRIX)
        state = code.encode_logical_qubit()
        circuit = Circuit(
            code.get_operation_circuit(operation=operation)
        )
        current_state = code.error_correcting_code_utilities.get_state_after_circuit(circuit=circuit,
                                                                                     qubit_order=code.all_qubits,
                                                                                     initial_state=state)
        expected_state = ExpectedStatesGenericFiveQubit().get_logical_minus_density_matrix()
        assert allclose(current_state.state, expected_state)

    def test_logical_h_corrects_in_hadamard_basis(self):
        code = GenericStabilizerCode(generators=get_check_matrix_values_5_qubit(), initial_logical_qubit_state=KET_ONE_DENSITY_MATRIX)
        state = code.encode_logical_qubit()
        circuit = Circuit(
            code.get_operation_circuit(operation=LogicalOperation(gate=LogicalGateLabel.H, qubit_index=0))
        )
        state_and_measurements = code.error_correcting_code_utilities.get_state_after_circuit(circuit=circuit,
                                                                                              qubit_order=code.all_qubits,
                                                                                              initial_state=state)
        state = state_and_measurements.state
        assert not allclose(state, ExpectedStatesGenericFiveQubit().get_logical_one_density_matrix())

        circuit = Circuit(
            code.get_error_circuit(Z, 0),
            code.get_error_correction_circuit(),
            code.get_operation_circuit(operation=LogicalOperation(gate=LogicalGateLabel.H, qubit_index=0)),
        )
        state_and_measurements = code.error_correcting_code_utilities.get_state_after_circuit(circuit=circuit,
                                                                                              qubit_order=code.all_qubits,
                                                                                              initial_state=state)
        assert allclose(state_and_measurements.state, ExpectedStatesGenericFiveQubit().get_logical_one_density_matrix())

    def test_logical_logical_z_has_logical_x_effect_after_logical_h(self):
        code = GenericStabilizerCode(generators=get_check_matrix_values_5_qubit(), initial_logical_qubit_state=KET_ZERO_DENSITY_MATRIX)
        state = code.encode_logical_qubit()
        circuit = Circuit(
            code.get_operation_circuit(operation=LogicalOperation(gate=LogicalGateLabel.H, qubit_index=0))
        )
        state_and_measurements = code.error_correcting_code_utilities.get_state_after_circuit(circuit=circuit,
                                                                                              qubit_order=code.all_qubits,
                                                                                              initial_state=state)
        state = state_and_measurements.state
        assert not allclose(state, ExpectedStatesGenericFiveQubit().get_logical_zero_density_matrix())

        circuit = Circuit(
            code.get_operation_circuit(operation=LogicalOperation(gate=LogicalGateLabel.Z, qubit_index=0)),
            code.get_operation_circuit(operation=LogicalOperation(gate=LogicalGateLabel.H, qubit_index=0))
        )
        state_and_measurements = code.error_correcting_code_utilities.get_state_after_circuit(circuit=circuit,
                                                                                              qubit_order=code.all_qubits,
                                                                                              initial_state=state)
        expected_state = ExpectedStatesGenericFiveQubit().get_logical_one_density_matrix()
        assert allclose(state_and_measurements.state, expected_state)

    def test_logical_logical_x_on_one_out_of_multiple_encoded_qubits(self):
        initial_state = tensor(KET_ZERO_DENSITY_MATRIX, KET_ZERO_DENSITY_MATRIX)
        code = GenericStabilizerCode(generators=get_check_matrix_values_4_qubit(), initial_logical_qubit_state=initial_state)

        state = code.encode_logical_qubit()
        circuit = Circuit(
            code.get_operation_circuit(operation=LogicalOperation(gate=LogicalGateLabel.X, qubit_index=1))
        )
        state_and_measurements = code.error_correcting_code_utilities.get_state_after_circuit(circuit=circuit,
                                                                                              qubit_order=code.all_qubits,
                                                                                              initial_state=state)

        expected_logical_state = tensor(KET_ZERO_DENSITY_MATRIX, KET_ONE_DENSITY_MATRIX)
        expected_state = GenericStabilizerCode(generators=get_check_matrix_values_4_qubit(),
                                               initial_logical_qubit_state=expected_logical_state).encode_logical_qubit()
        assert allclose(state_and_measurements.state, expected_state)

    def test_logical_h_on_one_out_of_multiple_encoded_qubits(self):
        code = GenericStabilizerCode(generators=get_check_matrix_values_4_qubit())

        state = code.encode_logical_qubit()
        circuit = Circuit(
            code.get_operation_circuit(operation=LogicalOperation(gate=LogicalGateLabel.H, qubit_index=1))
        )
        state_and_measurements = code.error_correcting_code_utilities.get_state_after_circuit(circuit=circuit,
                                                                                              qubit_order=code.all_qubits,
                                                                                              initial_state=state)

        expected_logical_state = tensor(KET_ZERO.state_vector(), KET_PLUS.state_vector())
        expected_state = GenericStabilizerCode(generators=get_check_matrix_values_4_qubit(),
                                               initial_logical_qubit_state=expected_logical_state).encode_logical_qubit()
        assert allclose(state_and_measurements.state, expected_state)

    def test_two_logical_h_on_one_out_of_multiple_encoded_qubits_is_identity(self):
        code = GenericStabilizerCode(generators=get_check_matrix_values_4_qubit())

        state = code.encode_logical_qubit()
        circuit = Circuit(
            code.get_operation_circuit(operation=LogicalOperation(gate=LogicalGateLabel.H, qubit_index=1)),
            code.get_operation_circuit(operation=LogicalOperation(gate=LogicalGateLabel.H, qubit_index=1))
        )
        state_and_measurements = code.error_correcting_code_utilities.get_state_after_circuit(circuit=circuit,
                                                                                              qubit_order=code.all_qubits,
                                                                                              initial_state=state)

        expected_state = GenericStabilizerCode(generators=get_check_matrix_values_4_qubit()).encode_logical_qubit()
        assert allclose(state_and_measurements.state, expected_state)

    def test_logical_logical_hzh_on_one_out_of_multiple_encoded_qubits_is_logical_x(self):
        code = GenericStabilizerCode(generators=get_check_matrix_values_4_qubit())

        state = code.encode_logical_qubit()
        circuit = Circuit(
            code.get_operation_circuit(operation=LogicalOperation(gate=LogicalGateLabel.H, qubit_index=1)),
            code.get_operation_circuit(operation=LogicalOperation(gate=LogicalGateLabel.Z, qubit_index=0)),
            code.get_operation_circuit(operation=LogicalOperation(gate=LogicalGateLabel.Z, qubit_index=1)),
            code.get_operation_circuit(operation=LogicalOperation(gate=LogicalGateLabel.H, qubit_index=1)),
        )
        state_and_measurements = code.error_correcting_code_utilities.get_state_after_circuit(circuit=circuit,
                                                                                              qubit_order=code.all_qubits,
                                                                                              initial_state=state)

        expected_logical_state = tensor(KET_ZERO.state_vector(), KET_ONE.state_vector())
        expected_state = GenericStabilizerCode(generators=get_check_matrix_values_4_qubit(),
                                               initial_logical_qubit_state=expected_logical_state).encode_logical_qubit()
        assert allclose(state_and_measurements.state, expected_state)

    def test_qubit_index_must_be_at_most_largest_logical_index(self):
        code = GenericStabilizerCode(generators=get_check_matrix_values_4_qubit())
        with pytest.raises(ValueError, match="Qubit index must be between 0 and 1. Was given 2."):
            code.get_operation_circuit(operation=LogicalOperation(gate=LogicalGateLabel.H, qubit_index=2))

        code = GenericStabilizerCode(generators=get_check_matrix_values_5_qubit())
        with pytest.raises(ValueError, match="Qubit index must be between 0 and 0. Was given 1."):
            code.get_operation_circuit(operation=LogicalOperation(gate=LogicalGateLabel.H, qubit_index=1))

    def test_multiqubit_encoding_corrects_errors_in_hadamard_basis(self):
        code = GenericStabilizerCode(generators=get_check_matrix_values_8_qubit())
        state = code.encode_logical_qubit()
        circuit = Circuit(
            code.get_operation_circuit(operation=LogicalOperation(gate=LogicalGateLabel.H, qubit_index=1)),
            code.get_error_circuit(Z, 0),
            code.get_error_correction_circuit(),
        )
        state_and_measurements = code.error_correcting_code_utilities.get_state_after_circuit(circuit=circuit,
                                                                                              qubit_order=code.all_qubits,
                                                                                              initial_state=state)

        expected_state_code = GenericStabilizerCode(generators=get_check_matrix_values_8_qubit())
        expected_state = code.encode_logical_qubit()
        circuit = Circuit(
            expected_state_code.get_operation_circuit(operation=LogicalOperation(gate=LogicalGateLabel.H, qubit_index=1))
        )
        expected_state = code.error_correcting_code_utilities.get_state_after_circuit(circuit=circuit,
                                                                                      qubit_order=code.all_qubits,
                                                                                      initial_state=expected_state)
        assert allclose(state_and_measurements.state, expected_state.state)
