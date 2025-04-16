import pytest
from cirq import KET_ONE, KET_PLUS, KET_ZERO, Z, kron
from numpy import allclose

from stim_experiments.error_correcting_codes.generic_stabilizer_code.generic_stabilizer_code import \
    GenericStabilizerCode
from stim_experiments.custom_dataclasses.logical_operation import LogicalGateLabel, LogicalOperation
from stim_experiments.utilities import KET_ONE_DENSITY_MATRIX, KET_PLUS_DENSITY_MATRIX, KET_ZERO_DENSITY_MATRIX
from tests.error_correcting_codes.generic_stabilizer_code.expected_states_generic_5_qubit import \
    ExpectedStatesGenericFiveQubit
from tests.error_correcting_codes.generic_stabilizer_code.utilities import get_check_matrix_values_4_qubit, \
    get_check_matrix_values_5_qubit, get_check_matrix_values_8_qubit


class TestLogicalGates:
    def test_logical_x(self):
        operation = LogicalOperation(gate=LogicalGateLabel.X, qubit_index=0)
        code = GenericStabilizerCode(generators=get_check_matrix_values_5_qubit())
        code.apply_operation(operation=operation)
        current_state = code.get_current_state()
        expected_state = ExpectedStatesGenericFiveQubit().get_logical_one_state_vector()
        assert allclose(current_state, expected_state)

    def test_logical_z(self):
        operation = LogicalOperation(gate=LogicalGateLabel.Z, qubit_index=0)
        code = GenericStabilizerCode(generators=get_check_matrix_values_5_qubit(), initial_logical_qubit_state=KET_PLUS_DENSITY_MATRIX)
        code.apply_operation(operation=operation)
        current_state = code.get_current_state()
        expected_state = ExpectedStatesGenericFiveQubit().get_logical_minus_density_matrix()
        assert allclose(current_state, expected_state)

    def test_logical_h_corrects_in_hadamard_basis(self):
        code = GenericStabilizerCode(generators=get_check_matrix_values_5_qubit(), initial_logical_qubit_state=KET_ONE_DENSITY_MATRIX)
        code.apply_operation(operation=LogicalOperation(gate=LogicalGateLabel.H, qubit_index=0))
        assert not allclose(code.get_current_state(), ExpectedStatesGenericFiveQubit().get_logical_one_density_matrix())
        code.apply_error(Z, 0)
        code.correct_errors()
        code.apply_operation(operation=LogicalOperation(gate=LogicalGateLabel.H, qubit_index=0))
        assert allclose(code.get_current_state(), ExpectedStatesGenericFiveQubit().get_logical_one_density_matrix())

    def test_logical_logical_z_has_logical_x_effect_after_logical_h(self):
        code = GenericStabilizerCode(generators=get_check_matrix_values_5_qubit(), initial_logical_qubit_state=KET_ZERO_DENSITY_MATRIX)
        code.apply_operation(operation=LogicalOperation(gate=LogicalGateLabel.H, qubit_index=0))
        assert not allclose(code.get_current_state(), ExpectedStatesGenericFiveQubit().get_logical_zero_density_matrix())

        code.apply_operation(operation=LogicalOperation(gate=LogicalGateLabel.Z, qubit_index=0))
        code.apply_operation(operation=LogicalOperation(gate=LogicalGateLabel.H, qubit_index=0))
        current_state = code.get_current_state()
        expected_state = ExpectedStatesGenericFiveQubit().get_logical_one_density_matrix()
        assert allclose(current_state, expected_state)

    def test_logical_logical_x_on_one_out_of_multiple_encoded_qubits(self):
        initial_state = kron(KET_ZERO_DENSITY_MATRIX, KET_ZERO_DENSITY_MATRIX)
        code = GenericStabilizerCode(generators=get_check_matrix_values_4_qubit(), initial_logical_qubit_state=initial_state)
        code.apply_operation(operation=LogicalOperation(gate=LogicalGateLabel.X, qubit_index=1))
        current_state = code.get_current_state()

        expected_logical_state = kron(KET_ZERO_DENSITY_MATRIX, KET_ONE_DENSITY_MATRIX)
        expected_state = GenericStabilizerCode(generators=get_check_matrix_values_4_qubit(), initial_logical_qubit_state=expected_logical_state).get_current_state()
        assert allclose(current_state, expected_state)

    def test_logical_h_on_one_out_of_multiple_encoded_qubits(self):
        code = GenericStabilizerCode(generators=get_check_matrix_values_4_qubit())
        code.apply_operation(operation=LogicalOperation(gate=LogicalGateLabel.H, qubit_index=1))
        current_state = code.get_current_state()

        expected_logical_state = kron(KET_ZERO.state_vector(), KET_PLUS.state_vector(), shape_len=1)
        expected_state = GenericStabilizerCode(generators=get_check_matrix_values_4_qubit(),
                                               initial_logical_qubit_state=expected_logical_state).get_current_state()
        assert allclose(current_state, expected_state)

    def test_two_logical_h_on_one_out_of_multiple_encoded_qubits_is_identity(self):
        code = GenericStabilizerCode(generators=get_check_matrix_values_4_qubit())
        code.apply_operation(operation=LogicalOperation(gate=LogicalGateLabel.H, qubit_index=1))
        code.apply_operation(operation=LogicalOperation(gate=LogicalGateLabel.H, qubit_index=1))
        current_state = code.get_current_state()

        expected_state = GenericStabilizerCode(generators=get_check_matrix_values_4_qubit()).get_current_state()
        assert allclose(current_state, expected_state)

    def test_logical_logical_hzh_on_one_out_of_multiple_encoded_qubits_is_logical_x(self):
        code = GenericStabilizerCode(generators=get_check_matrix_values_4_qubit())
        code.apply_operation(operation=LogicalOperation(gate=LogicalGateLabel.H, qubit_index=1))
        code.apply_operation(operation=LogicalOperation(gate=LogicalGateLabel.Z, qubit_index=0))
        code.apply_operation(operation=LogicalOperation(gate=LogicalGateLabel.Z, qubit_index=1))
        code.apply_operation(operation=LogicalOperation(gate=LogicalGateLabel.H, qubit_index=1))
        current_state = code.get_current_state()

        expected_logical_state = kron(KET_ZERO.state_vector(), KET_ONE.state_vector(), shape_len=1)
        expected_state = GenericStabilizerCode(generators=get_check_matrix_values_4_qubit(), initial_logical_qubit_state=expected_logical_state).get_current_state()
        assert allclose(current_state, expected_state)

    def test_qubit_index_must_be_at_most_largest_logical_index(self):
        code = GenericStabilizerCode(generators=get_check_matrix_values_4_qubit())
        with pytest.raises(ValueError, match="Qubit index must be between 0 and 1. Was given 2."):
            code.apply_operation(operation=LogicalOperation(gate=LogicalGateLabel.H, qubit_index=2))

        code = GenericStabilizerCode(generators=get_check_matrix_values_5_qubit())
        with pytest.raises(ValueError, match="Qubit index must be between 0 and 0. Was given 1."):
            code.apply_operation(operation=LogicalOperation(gate=LogicalGateLabel.H, qubit_index=1))

    def test_multiqubit_encoding_corrects_errors_in_hadamard_basis(self):
        code = GenericStabilizerCode(generators=get_check_matrix_values_8_qubit())
        code.apply_operation(operation=LogicalOperation(gate=LogicalGateLabel.H, qubit_index=1))
        code.apply_error(Z, 0)
        code.correct_errors()
        current_state = code.get_current_state()

        expected_state_code = GenericStabilizerCode(generators=get_check_matrix_values_8_qubit())
        expected_state_code.apply_operation(operation=LogicalOperation(gate=LogicalGateLabel.H, qubit_index=1))
        expected_state = expected_state_code.get_current_state()
        assert allclose(current_state, expected_state)
