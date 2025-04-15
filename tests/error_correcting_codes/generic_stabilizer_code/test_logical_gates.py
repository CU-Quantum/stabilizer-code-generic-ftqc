from cirq import KET_ONE, KET_ZERO, Z, density_matrix_from_state_vector, kron
from numpy import allclose, sqrt

from stim_experiments.error_correcting_codes.generic_stabilizer_code.generic_stabilizer_code import \
    GenericStabilizerCode
from stim_experiments.simulators.custom_dataclasses.logical_operation import LogicalGateLabel, LogicalOperation
from stim_experiments.utilities import KET_ONE_DENSITY_MATRIX, KET_PLUS_DENSITY_MATRIX, KET_ZERO_DENSITY_MATRIX
from tests.error_correcting_codes.generic_stabilizer_code.expected_states_generic_5_qubit import \
    ExpectedStatesGenericFiveQubit
from tests.error_correcting_codes.generic_stabilizer_code.utilities import get_check_matrix_values_4_qubit, \
    get_check_matrix_values_5_qubit


class TestLogicalGates:
    def test_logical_x(self):
        operation = LogicalOperation(gate=LogicalGateLabel.X, qubit_index=0)
        code = GenericStabilizerCode(generators=get_check_matrix_values_5_qubit())
        code.apply_operation(operation=operation)
        current_state = code.get_current_state()
        expected_state = ExpectedStatesGenericFiveQubit().get_logical_one_density_matrix()
        assert allclose(current_state, expected_state)


    def test_logical_z(self):
        operation = LogicalOperation(gate=LogicalGateLabel.Z, qubit_index=0)
        code = GenericStabilizerCode(generators=get_check_matrix_values_5_qubit(), initial_logical_qubit_state_density_matrix=KET_PLUS_DENSITY_MATRIX)
        code.apply_operation(operation=operation)
        current_state = code.get_current_state()
        expected_state = ExpectedStatesGenericFiveQubit().get_logical_minus_density_matrix()
        assert allclose(current_state, expected_state)


    def test_logical_h_corrects_in_hadamard_basis(self):
        code = GenericStabilizerCode(generators=get_check_matrix_values_5_qubit(), initial_logical_qubit_state_density_matrix=KET_ONE_DENSITY_MATRIX)
        code.apply_operation(operation=LogicalOperation(gate=LogicalGateLabel.H, qubit_index=0))
        assert not allclose(code.get_current_state(), ExpectedStatesGenericFiveQubit().get_logical_one_density_matrix())
        code.apply_error(Z, 0)
        code.correct_errors()
        code.apply_operation(operation=LogicalOperation(gate=LogicalGateLabel.H, qubit_index=0))
        assert allclose(code.get_current_state(), ExpectedStatesGenericFiveQubit().get_logical_one_density_matrix())


    def test_logical_logical_z_has_logical_x_effect_after_logical_h(self):
        code = GenericStabilizerCode(generators=get_check_matrix_values_5_qubit())
        code.apply_operation(operation=LogicalOperation(gate=LogicalGateLabel.H, qubit_index=0))
        assert not allclose(code.get_current_state(), ExpectedStatesGenericFiveQubit().get_logical_zero_density_matrix())

        code.apply_operation(operation=LogicalOperation(gate=LogicalGateLabel.Z, qubit_index=0))
        code.apply_operation(operation=LogicalOperation(gate=LogicalGateLabel.H, qubit_index=0))
        current_state = code.get_current_state()
        expected_state = ExpectedStatesGenericFiveQubit().get_logical_one_density_matrix()
        assert allclose(current_state, expected_state)


    def test_logical_logical_x_on_one_out_of_multiple_encoded_qubits(self):
        code = GenericStabilizerCode(generators=get_check_matrix_values_4_qubit())
        code.apply_operation(operation=LogicalOperation(gate=LogicalGateLabel.X, qubit_index=1))
        current_state = code.get_current_state()

        expected_logical_state = kron(KET_ZERO_DENSITY_MATRIX, KET_ONE_DENSITY_MATRIX)
        expected_state = GenericStabilizerCode(generators=get_check_matrix_values_4_qubit(), initial_logical_qubit_state_density_matrix=expected_logical_state).get_current_state()
        assert allclose(current_state, expected_state)

    # def test_logical_h_on_one_out_of_multiple_encoded_qubits(self):
    #     code = GenericStabilizerCode(generators=get_check_matrix_values_4_qubit())
    #     code.apply_operation(operation=LogicalOperation(gate=LogicalGateLabel.H, qubit_index=1))
    #     current_state = code.get_current_state()
    #
    #     expected_logical_state = kron(KET_ZERO.state_vector(), (1/sqrt(2)) * (KET_ZERO.state_vector() + KET_ONE.state_vector()))
    #     expected_logical_state = kron(KET_ZERO.state_vector(), KET_ONE.state_vector())


    def test_logical_logical_h_on_one_out_of_multiple_encoded_qubits(self):
        initial_logical_state = kron(KET_ZERO.state_vector(), KET_ZERO.state_vector())
        code = GenericStabilizerCode(generators=get_check_matrix_values_4_qubit(), initial_logical_qubit_state_density_matrix=initial_logical_state)
        code.apply_operation(operation=LogicalOperation(gate=LogicalGateLabel.H, qubit_index=1))
        code.apply_operation(operation=LogicalOperation(gate=LogicalGateLabel.Z, qubit_index=0))
        code.apply_operation(operation=LogicalOperation(gate=LogicalGateLabel.Z, qubit_index=1))
        code.apply_operation(operation=LogicalOperation(gate=LogicalGateLabel.H, qubit_index=1))
        current_state = code.get_current_state()

        # expected_logical_state = kron(KET_ZERO.state_vector(), (1/sqrt(2)) * (KET_ZERO.state_vector() + KET_ONE.state_vector()))
        expected_logical_state = kron(KET_ZERO.state_vector(), KET_ONE.state_vector())
        # expected_logical_state = kron(KET_ZERO.state_vector(), KET_ZERO.state_vector())
        expected_state = GenericStabilizerCode(generators=get_check_matrix_values_4_qubit(), initial_logical_qubit_state_density_matrix=expected_logical_state).get_current_state()
        assert allclose(current_state, expected_state)
