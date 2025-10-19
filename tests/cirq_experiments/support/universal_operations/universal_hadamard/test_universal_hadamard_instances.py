import numpy as np
import pytest
from cirq import Circuit
from numpy import array

from cirq_experiments.custom_dataclasses.simulation_operation import LogicalEncodingIndex
from cirq_experiments.error_correcting_codes.repetition_code.repetition_code import RepetitionCodeOneLogical
from cirq_experiments.error_correcting_codes.stabilizer_standardized_code.stabilizer_standardized_code import \
    StabilizerStandardizedCode
from cirq_experiments.support.universal_operations.universal_hadamard.universal_hadamard import UniversalHadamard
from cirq_experiments.support.universal_operations.universal_hadamard.universal_hadamard_fault_tolerant import \
    UniversalHadamardFaultTolerant
from cirq_experiments.support.universal_operations.universal_hadamard.universal_hadamard_single_ancilla import \
    UniversalHadamardSingleAncilla
from cirq_experiments.globals.fresh_ancillas_pool import FreshAncillasPool
from cirq_experiments.simulations.error_correcting_simulator import get_error_correcting_simulator
from cirq_experiments.utilities.predefined_check_matrix_values import get_check_matrix_values_4_qubit
from cirq_experiments.utilities.utilities import states_are_equal
from tests.cirq_experiments.utilities_for_tests import get_random_encoded_initial_state, random_complex_unit_vector, \
    set_configuration_to_reduce_ancilla_qubits, set_seed


class TestUniversalHadamard:
    @pytest.fixture(autouse=True, params=range(3))
    def _seed(self, request):
        set_seed(seed=request.param)
        set_configuration_to_reduce_ancilla_qubits()

    @pytest.mark.parametrize('universal_hadamard_type', [
        pytest.param(UniversalHadamardSingleAncilla, id='UniversalHadamardSingleAncilla'),
        pytest.param(UniversalHadamardFaultTolerant, id='UniversalHadamardFaultTolerant'),
    ])
    def test_random_alpha_beta(self, universal_hadamard_type: type[UniversalHadamard]):
        code = RepetitionCodeOneLogical(num_qubits=1)
        universal_hadamard = universal_hadamard_type(code=LogicalEncodingIndex(encoding=code, qubit_index_relative=0))
        FreshAncillasPool().set_first_ancilla_num(first_ancilla_num=len(code.data_qubits))

        initial_state = random_complex_unit_vector(num_qubits=1)
        utilities = get_error_correcting_simulator(state=initial_state)

        simulated_state = utilities.run_simulation(
            circuit=Circuit(
                code.encode_logical_qubit(),
                universal_hadamard.get_hadamard_circuit(),
            ),
            num_data_qubits=len(code.data_qubits),
            initial_data_state=initial_state,
        ).state
        expected_state = (1 / np.sqrt(2)) * array([initial_state[0] + initial_state[1], initial_state[0] - initial_state[1]])
        assert states_are_equal(simulated_state, expected_state)

    @pytest.mark.parametrize('universal_hadamard_type', [
        pytest.param(UniversalHadamardSingleAncilla, id='UniversalHadamardSingleAncilla'),
        pytest.param(UniversalHadamardFaultTolerant, id='UniversalHadamardFaultTolerant'),
    ])
    def test_multiple_qubit_encoding_hadamard_one_qubit(self, universal_hadamard_type: type[UniversalHadamard]):
        code = StabilizerStandardizedCode(generators=get_check_matrix_values_4_qubit())
        universal_hadamard = universal_hadamard_type(code=LogicalEncodingIndex(encoding=code, qubit_index_relative=1))
        FreshAncillasPool().set_first_ancilla_num(first_ancilla_num=len(code.data_qubits))

        encoded_initial_state = get_random_encoded_initial_state(code=code)
        initial_state = encoded_initial_state.initial_state
        initial_coefficients = encoded_initial_state.initial_coefficients
        computational_basis_states = encoded_initial_state.computational_basis_states
        utilities = get_error_correcting_simulator(state=initial_state)

        simulated_state = utilities.run_simulation(
            circuit=Circuit(
                code.encode_logical_qubit(),
                universal_hadamard.get_hadamard_circuit(),
            ),
            num_data_qubits=len(code.data_qubits),
            initial_data_state=initial_state,
        ).state

        expected_state = (
                (initial_coefficients[0] + initial_coefficients[1]) * computational_basis_states[0]
                + (initial_coefficients[0] - initial_coefficients[1]) * computational_basis_states[1]
                + (initial_coefficients[2] + initial_coefficients[3]) * computational_basis_states[2]
                + (initial_coefficients[2] - initial_coefficients[3]) * computational_basis_states[3]
        )
        assert states_are_equal(simulated_state, expected_state)
