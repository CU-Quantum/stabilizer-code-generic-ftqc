from cirq import Circuit, LineQubit, X
from numpy import sqrt

from stim_experiments.custom_dataclasses.logical_operation import LogicalGateLabel, LogicalOperation
from stim_experiments.custom_dataclasses.simulation_operation import LogicalEncodingIndex
from stim_experiments.error_correcting_codes.stabilizer_standardized_code.stabilizer_standardized_code import \
    StabilizerStandardizedCode
from stim_experiments.error_correcting_codes.support.universal_operations.universal_hadamard.universal_hadamard_single_ancilla import \
    UniversalHadamardSingleAncilla
from stim_experiments.globals.fresh_ancillas_pool import FreshAncillasPool
from stim_experiments.simulations.error_correcting_simulator import get_error_correcting_simulator
from stim_experiments.utilities.predefined_check_matrix_values import get_check_matrix_values_4_qubit, \
    get_check_matrix_values_5_qubit, get_check_matrix_values_8_qubit
from stim_experiments.utilities.utilities import KET_ONE_STATE_VECTOR, KET_PLUS_STATE_VECTOR, KET_ZERO_STATE_VECTOR, \
    states_are_equal, tensor
from tests.error_correcting_codes.stabilizer_standardized_code.expected_states_standardized_5_qubit import \
    ExpectedStatesGenericFiveQubit


class TestUniversalHadamardSingleAncilla:
    def test_logical_z_has_logical_x_effect_after_logical_h(self):
        code = StabilizerStandardizedCode(generators=get_check_matrix_values_5_qubit())
        FreshAncillasPool().set_first_ancilla_num(first_ancilla_num=len(code.data_qubits))

        hadamard_circuit = UniversalHadamardSingleAncilla(code=LogicalEncodingIndex(encoding=code, qubit_index_relative=0)).get_hadamard_circuit()
        circuit = Circuit(
            code.encode_logical_qubit(),
            hadamard_circuit,
            code.get_operation_circuit(operation=LogicalOperation(gate=LogicalGateLabel.Z, qubit_index=0)),
            hadamard_circuit,
        )

        initial_data_state = ExpectedStatesGenericFiveQubit().get_logical_zero_state_vector()
        utilities = get_error_correcting_simulator(state=initial_data_state)
        state = utilities.run_simulation(
            circuit=circuit,
            num_data_qubits=len(code.data_qubits),
            initial_data_state=initial_data_state,
        ).state
        expected_state = ExpectedStatesGenericFiveQubit().get_logical_one_state_vector()
        assert states_are_equal(state, expected_state)

    def test_logical_h_on_one_out_of_multiple_encoded_qubits(self):
        code = StabilizerStandardizedCode(generators=get_check_matrix_values_4_qubit())
        FreshAncillasPool().set_first_ancilla_num(first_ancilla_num=len(code.data_qubits))
        hadamard_circuit = UniversalHadamardSingleAncilla(code=LogicalEncodingIndex(encoding=code, qubit_index_relative=1)).get_hadamard_circuit()
        circuit = Circuit(
            code.encode_logical_qubit(),
            hadamard_circuit,
        )

        initial_data_state = tensor(*[KET_ZERO_STATE_VECTOR] * len(code.data_qubits))
        utilities = get_error_correcting_simulator(state=initial_data_state)
        state_and_measurements = utilities.run_simulation(circuit=circuit,
                                                          num_data_qubits=len(code.data_qubits),
                                                          initial_data_state=initial_data_state)

        expected_state = utilities.run_simulation(
            circuit=Circuit(
                code.encode_logical_qubit(),
            ),
            num_data_qubits=len(code.data_qubits),
            initial_data_state=tensor(*[KET_ZERO_STATE_VECTOR] * 3, KET_PLUS_STATE_VECTOR)
        ).state
        assert states_are_equal(state_and_measurements.state, expected_state)

    def test_two_logical_h_on_one_out_of_multiple_encoded_qubits_is_identity(self):
        code = StabilizerStandardizedCode(generators=get_check_matrix_values_4_qubit())
        FreshAncillasPool().set_first_ancilla_num(first_ancilla_num=len(code.data_qubits))
        hadamard_circuit = UniversalHadamardSingleAncilla(code=LogicalEncodingIndex(encoding=code, qubit_index_relative=1)).get_hadamard_circuit()
        circuit = Circuit(
            code.encode_logical_qubit(),
            hadamard_circuit,
            hadamard_circuit,
        )

        initial_data_state = tensor(*[KET_ZERO_STATE_VECTOR] * len(code.data_qubits))
        utilities = get_error_correcting_simulator(state=initial_data_state)
        state_and_measurements = utilities.run_simulation(circuit=circuit,
                                                          num_data_qubits=len(code.data_qubits),
                                                          initial_data_state=initial_data_state)
        expected_state = utilities.run_simulation(
            circuit=Circuit(
                code.encode_logical_qubit(),
            ),
            num_data_qubits=len(code.data_qubits),
            initial_data_state=initial_data_state
        ).state
        assert states_are_equal(state_and_measurements.state, expected_state)

    def test_logical_hzh_on_one_out_of_multiple_encoded_qubits_is_logical_x(self):
        code = StabilizerStandardizedCode(generators=get_check_matrix_values_4_qubit())
        FreshAncillasPool().set_first_ancilla_num(first_ancilla_num=len(code.data_qubits))

        initial_data_state = tensor(*[KET_ZERO_STATE_VECTOR] * len(code.data_qubits))
        utilities = get_error_correcting_simulator(state=initial_data_state)

        hadamard_circuit = UniversalHadamardSingleAncilla(code=LogicalEncodingIndex(encoding=code, qubit_index_relative=1)).get_hadamard_circuit()
        simulated_state = utilities.run_simulation(
            circuit=Circuit(
                code.encode_logical_qubit(),
                hadamard_circuit,
                code.get_operation_circuit(operation=LogicalOperation(gate=LogicalGateLabel.Z, qubit_index=0)),
                code.get_operation_circuit(operation=LogicalOperation(gate=LogicalGateLabel.Z, qubit_index=1)),
                hadamard_circuit,
            ),
            num_data_qubits=len(code.data_qubits),
            initial_data_state=initial_data_state
        ).state
        expected_state = utilities.run_simulation(
            circuit=Circuit(
                code.encode_logical_qubit(),
            ),
            num_data_qubits=len(code.data_qubits),
            initial_data_state=tensor(*[KET_ZERO_STATE_VECTOR] * 3, KET_ONE_STATE_VECTOR)
        ).state
        assert states_are_equal(simulated_state, expected_state)

    def test_multiqubit_encoding_corrects_errors_in_hadamard_basis(self):
        code = StabilizerStandardizedCode(generators=get_check_matrix_values_8_qubit())
        FreshAncillasPool().set_first_ancilla_num(first_ancilla_num=len(code.data_qubits))

        initial_data_state = tensor(*[KET_ZERO_STATE_VECTOR] * len(code.data_qubits))
        utilities = get_error_correcting_simulator(state=initial_data_state)

        arbitrary_error = X(LineQubit(0))
        hadamard_circuit = UniversalHadamardSingleAncilla(code=LogicalEncodingIndex(encoding=code, qubit_index_relative=1)).get_hadamard_circuit()
        simulated_state = utilities.run_simulation(
            circuit=Circuit(
                code.encode_logical_qubit(),
                hadamard_circuit,
                arbitrary_error,
                code.get_error_correction_circuit(),
            ),
            num_data_qubits=len(code.data_qubits),
            initial_data_state=initial_data_state
        ).state

        a_logical_hadamard_basis = (1 / sqrt(2)) * (
            tensor(*[KET_ZERO_STATE_VECTOR] * 8)
            + tensor(*[KET_ZERO_STATE_VECTOR] * 4, KET_ONE_STATE_VECTOR, KET_ZERO_STATE_VECTOR, KET_ONE_STATE_VECTOR, KET_ZERO_STATE_VECTOR)
        )
        expected_state = utilities.run_simulation(
            circuit=Circuit(
                code.encode_logical_qubit(),
            ),
            num_data_qubits=len(code.data_qubits),
            initial_data_state=a_logical_hadamard_basis
        ).state
        assert states_are_equal(simulated_state, expected_state)
