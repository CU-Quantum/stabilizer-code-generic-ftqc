import pytest
from cirq import Circuit, LineQubit, X
from numpy import sqrt

from stim_experiments.error_correcting_codes.error_correcting_code_utilities import get_error_correcting_code_utilities
from stim_experiments.error_correcting_codes.stabilizer_code_standardized.code_standardized_standardized import \
    GenericStabilizerCode
from stim_experiments.custom_dataclasses.logical_operation import LogicalGateLabel, LogicalOperation
from stim_experiments.globals.fresh_ancillas_pool import FreshAncillasPool
from stim_experiments.utilities.utilities import KET_ONE_STATE_VECTOR, KET_PLUS_STATE_VECTOR, KET_ZERO_STATE_VECTOR, \
    tensor
from tests.error_correcting_codes.generic_stabilizer_code.expected_states_generic_5_qubit import \
    ExpectedStatesGenericFiveQubit
from stim_experiments.utilities.predefined_check_matrix_values import get_check_matrix_values_4_qubit, \
    get_check_matrix_values_5_qubit, get_check_matrix_values_8_qubit
from tests.utilities import states_are_equal


class TestGenericStabilizer:
    def test_logical_z_has_logical_x_effect_after_logical_h(self):
        code = GenericStabilizerCode(generators=get_check_matrix_values_5_qubit())
        FreshAncillasPool().set_first_ancilla_num(first_ancilla_num=len(code.data_qubits))
        circuit = Circuit(
            code.encode_logical_qubit(),
            code.get_operation_circuit(operation=LogicalOperation(gate=LogicalGateLabel.H, qubit_index=0)),
            code.get_operation_circuit(operation=LogicalOperation(gate=LogicalGateLabel.Z, qubit_index=0)),
            code.get_operation_circuit(operation=LogicalOperation(gate=LogicalGateLabel.H, qubit_index=0)),

        )

        initial_data_state = ExpectedStatesGenericFiveQubit().get_logical_zero_state_vector()
        utilities = get_error_correcting_code_utilities(state=initial_data_state)
        state_and_measurements = utilities.get_state_after_circuit(circuit=circuit,
                                                                   num_data_qubits=len(code.data_qubits),
                                                                   initial_data_state=initial_data_state)
        expected_state = ExpectedStatesGenericFiveQubit().get_logical_one_state_vector()
        assert states_are_equal(state_and_measurements.state, expected_state)

    def test_logical_x_on_one_out_of_multiple_encoded_qubits(self):
        code = GenericStabilizerCode(generators=get_check_matrix_values_4_qubit())
        FreshAncillasPool().set_first_ancilla_num(first_ancilla_num=len(code.data_qubits))
        circuit = Circuit(
            code.encode_logical_qubit(),
            code.get_operation_circuit(operation=LogicalOperation(gate=LogicalGateLabel.X, qubit_index=1))
        )

        initial_data_state = tensor(*[KET_ZERO_STATE_VECTOR] * len(code.data_qubits))
        utilities = get_error_correcting_code_utilities(state=initial_data_state)
        state_and_measurements = utilities.get_state_after_circuit(circuit=circuit,
                                                                   num_data_qubits=len(code.data_qubits),
                                                                   initial_data_state=initial_data_state)

        expected_state = utilities.get_state_after_circuit(
            circuit=Circuit(
                code.encode_logical_qubit(),
            ),
            num_data_qubits=len(code.data_qubits),
            initial_data_state=tensor(*[KET_ZERO_STATE_VECTOR] * 3, KET_ONE_STATE_VECTOR)
        ).state
        assert states_are_equal(state_and_measurements.state, expected_state)

    def test_logical_h_on_one_out_of_multiple_encoded_qubits(self):
        code = GenericStabilizerCode(generators=get_check_matrix_values_4_qubit())
        FreshAncillasPool().set_first_ancilla_num(first_ancilla_num=len(code.data_qubits))
        circuit = Circuit(
            code.encode_logical_qubit(),
            code.get_operation_circuit(operation=LogicalOperation(gate=LogicalGateLabel.H, qubit_index=1))
        )

        initial_data_state = tensor(*[KET_ZERO_STATE_VECTOR] * len(code.data_qubits))
        utilities = get_error_correcting_code_utilities(state=initial_data_state)
        state_and_measurements = utilities.get_state_after_circuit(circuit=circuit,
                                                                   num_data_qubits=len(code.data_qubits),
                                                                   initial_data_state=initial_data_state)

        expected_state = utilities.get_state_after_circuit(
            circuit=Circuit(
                code.encode_logical_qubit(),
            ),
            num_data_qubits=len(code.data_qubits),
            initial_data_state=tensor(*[KET_ZERO_STATE_VECTOR] * 3, KET_PLUS_STATE_VECTOR)
        ).state
        assert states_are_equal(state_and_measurements.state, expected_state)

    def test_two_logical_h_on_one_out_of_multiple_encoded_qubits_is_identity(self):
        code = GenericStabilizerCode(generators=get_check_matrix_values_4_qubit())
        FreshAncillasPool().set_first_ancilla_num(first_ancilla_num=len(code.data_qubits))
        circuit = Circuit(
            code.encode_logical_qubit(),
            code.get_operation_circuit(operation=LogicalOperation(gate=LogicalGateLabel.H, qubit_index=1)),
            code.get_operation_circuit(operation=LogicalOperation(gate=LogicalGateLabel.H, qubit_index=1))
        )

        initial_data_state = tensor(*[KET_ZERO_STATE_VECTOR] * len(code.data_qubits))
        utilities = get_error_correcting_code_utilities(state=initial_data_state)
        state_and_measurements = utilities.get_state_after_circuit(circuit=circuit,
                                                                   num_data_qubits=len(code.data_qubits),
                                                                   initial_data_state=initial_data_state)
        expected_state = utilities.get_state_after_circuit(
            circuit=Circuit(
                code.encode_logical_qubit(),
            ),
            num_data_qubits=len(code.data_qubits),
            initial_data_state=initial_data_state
        ).state
        assert states_are_equal(state_and_measurements.state, expected_state)

    def test_logical_hzh_on_one_out_of_multiple_encoded_qubits_is_logical_x(self):
        code = GenericStabilizerCode(generators=get_check_matrix_values_4_qubit())
        FreshAncillasPool().set_first_ancilla_num(first_ancilla_num=len(code.data_qubits))

        initial_data_state = tensor(*[KET_ZERO_STATE_VECTOR] * len(code.data_qubits))
        utilities = get_error_correcting_code_utilities(state=initial_data_state)

        simulated_state = utilities.get_state_after_circuit(
            circuit=Circuit(
                code.encode_logical_qubit(),
                code.get_operation_circuit(operation=LogicalOperation(gate=LogicalGateLabel.H, qubit_index=1)),
                code.get_operation_circuit(operation=LogicalOperation(gate=LogicalGateLabel.Z, qubit_index=0)),
                code.get_operation_circuit(operation=LogicalOperation(gate=LogicalGateLabel.Z, qubit_index=1)),
                code.get_operation_circuit(operation=LogicalOperation(gate=LogicalGateLabel.H, qubit_index=1)),
            ),
            num_data_qubits=len(code.data_qubits),
            initial_data_state=initial_data_state
        ).state
        expected_state = utilities.get_state_after_circuit(
            circuit=Circuit(
                code.encode_logical_qubit(),
            ),
            num_data_qubits=len(code.data_qubits),
            initial_data_state=tensor(*[KET_ZERO_STATE_VECTOR] * 3, KET_ONE_STATE_VECTOR)
        ).state
        assert states_are_equal(simulated_state, expected_state)

    def test_qubit_index_must_be_at_most_largest_logical_index(self):
        code = GenericStabilizerCode(generators=get_check_matrix_values_4_qubit())
        with pytest.raises(ValueError, match="Qubit index must be between 0 and 1. Was given 2."):
            code.get_operation_circuit(operation=LogicalOperation(gate=LogicalGateLabel.H, qubit_index=2))

        code = GenericStabilizerCode(generators=get_check_matrix_values_5_qubit())
        with pytest.raises(ValueError, match="Qubit index must be between 0 and 0. Was given 1."):
            code.get_operation_circuit(operation=LogicalOperation(gate=LogicalGateLabel.H, qubit_index=1))

    def test_multiqubit_encoding_corrects_errors_in_hadamard_basis(self):
        code = GenericStabilizerCode(generators=get_check_matrix_values_8_qubit())
        FreshAncillasPool().set_first_ancilla_num(first_ancilla_num=len(code.data_qubits))

        initial_data_state = tensor(*[KET_ZERO_STATE_VECTOR] * len(code.data_qubits))
        utilities = get_error_correcting_code_utilities(state=initial_data_state)

        arbitrary_error = X(LineQubit(0))
        simulated_state = utilities.get_state_after_circuit(
            circuit=Circuit(
                code.encode_logical_qubit(),
                code.get_operation_circuit(operation=LogicalOperation(gate=LogicalGateLabel.H, qubit_index=1)),
                arbitrary_error,
                code.get_error_correction_circuit(),
            ),
            num_data_qubits=len(code.data_qubits),
            initial_data_state=initial_data_state
        ).state

        a_logical_hadamard_basis = (1/sqrt(2)) * (
            tensor(*[KET_ZERO_STATE_VECTOR] * 8)
            + tensor(*[KET_ZERO_STATE_VECTOR] * 4, KET_ONE_STATE_VECTOR, KET_ZERO_STATE_VECTOR, KET_ONE_STATE_VECTOR, KET_ZERO_STATE_VECTOR)
        )
        expected_state = utilities.get_state_after_circuit(
            circuit=Circuit(
                code.encode_logical_qubit(),
            ),
            num_data_qubits=len(code.data_qubits),
            initial_data_state=a_logical_hadamard_basis
        ).state
        assert states_are_equal(simulated_state, expected_state)
