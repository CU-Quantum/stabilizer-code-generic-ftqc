import numpy as np
import pytest
from cirq import Circuit

from stim_experiments.custom_dataclasses.simulation_operation import LogicalEncodingIndex
from stim_experiments.error_correcting_codes.error_correcting_code_utilities import get_error_correcting_code_utilities
from stim_experiments.error_correcting_codes.repetition_code.repetition_code import RepetitionCode
from stim_experiments.error_correcting_codes.stabilizer_standardized_code.stabilizer_standardized_code import \
    StabilizerStandardizedCode
from stim_experiments.error_correcting_codes.support.universal_operations.universal_t.universal_t import \
    UniversalT
from stim_experiments.error_correcting_codes.support.universal_operations.universal_t.universal_t_fault_tolerant import \
    UniversalTFaultTolerant
from stim_experiments.error_correcting_codes.support.universal_operations.universal_t.universal_t_singe_ancilla import \
    UniversalTSingleAncilla
from stim_experiments.globals.fresh_ancillas_pool import FreshAncillasPool
from stim_experiments.utilities.predefined_check_matrix_values import get_check_matrix_values_4_qubit
from stim_experiments.utilities.utilities import states_are_equal
from tests.utilities import get_random_encoded_initial_state, set_configuration_to_reduce_ancilla_qubits, set_seed


T_ROTATION = np.exp(1j * np.pi / 4)


class TestUniversalTInstances:
    @pytest.fixture(autouse=True, params=range(3))
    def _seed(self, request):
        set_seed(seed=request.param)

    @pytest.mark.parametrize('universal_t_type', [
        pytest.param(UniversalTFaultTolerant, id='UniversalTFaultTolerant'),
        pytest.param(UniversalTSingleAncilla, id='UniversalTSingleAncilla'),
    ])
    def test_random_alpha_beta(self, universal_t_type: type[UniversalT]):
        set_configuration_to_reduce_ancilla_qubits()
        code = RepetitionCode(num_qubits=1)
        FreshAncillasPool().set_first_ancilla_num(first_ancilla_num=len(code.data_qubits))
        universal_t = universal_t_type(code=LogicalEncodingIndex(encoding=code, qubit_index_relative=0))

        encoded_initial_state = get_random_encoded_initial_state(code=code)
        initial_state = encoded_initial_state.initial_state
        utilities = get_error_correcting_code_utilities(state=initial_state)

        simulated_state = utilities.get_state_after_circuit(
            circuit=Circuit(
                code.encode_logical_qubit(),
                universal_t.get_t_circuit(),
            ),
            num_data_qubits=len(code.data_qubits),
            initial_data_state=initial_state,
        ).state
        expected_state = (
                encoded_initial_state.initial_coefficients[0] * encoded_initial_state.computational_basis_states[0]
                + T_ROTATION * encoded_initial_state.initial_coefficients[1] * encoded_initial_state.computational_basis_states[1]
        )
        assert states_are_equal(simulated_state, expected_state)

    @pytest.mark.parametrize('universal_t_type', [
        pytest.param(UniversalTFaultTolerant, id='UniversalTFaultTolerant'),
        pytest.param(UniversalTSingleAncilla, id='UniversalTSingleAncilla'),
    ])
    def test_multiple_qubit_encoding_t_one_qubit(self, universal_t_type: type[UniversalT]):
        set_configuration_to_reduce_ancilla_qubits()
        code = StabilizerStandardizedCode(generators=get_check_matrix_values_4_qubit())
        universal_t = universal_t_type(code=LogicalEncodingIndex(encoding=code, qubit_index_relative=1))
        FreshAncillasPool().set_first_ancilla_num(first_ancilla_num=len(code.data_qubits))

        encoded_initial_state = get_random_encoded_initial_state(code=code)
        initial_state = encoded_initial_state.initial_state
        initial_coefficients = encoded_initial_state.initial_coefficients
        computational_basis_states = encoded_initial_state.computational_basis_states
        utilities = get_error_correcting_code_utilities(state=initial_state)

        simulated_state = utilities.get_state_after_circuit(
            circuit=Circuit(
                code.encode_logical_qubit(),
                universal_t.get_t_circuit(),
            ),
            num_data_qubits=len(code.data_qubits),
            initial_data_state=initial_state,
        ).state

        expected_state = (
                initial_coefficients[0] * computational_basis_states[0]
                + T_ROTATION * initial_coefficients[1] * computational_basis_states[1]
                + initial_coefficients[2] * computational_basis_states[2]
                + T_ROTATION * initial_coefficients[3] * computational_basis_states[3]
        )
        assert states_are_equal(simulated_state, expected_state)
