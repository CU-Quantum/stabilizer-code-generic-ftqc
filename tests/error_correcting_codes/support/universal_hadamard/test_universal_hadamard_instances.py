import random

import numpy as np
import pytest
from cirq import Circuit, X
from numpy import array

from stim_experiments.custom_dataclasses.logical_operation import LogicalGateLabel, LogicalOperation
from stim_experiments.error_correcting_codes.error_correcting_code_utilities import get_error_correcting_code_utilities
from stim_experiments.error_correcting_codes.five_qubit_code.five_qubit_code import FiveQubitCode
from stim_experiments.error_correcting_codes.repetition_code.repetition_code import RepetitionCode
from stim_experiments.error_correcting_codes.stabilizer_standardized_code.stabilizer_standardized_code import \
    StabilizerStandardizedCode
from stim_experiments.error_correcting_codes.support.universal_hadamard.universal_hadamard import UniversalHadamard
from stim_experiments.error_correcting_codes.support.universal_hadamard.universal_hadamard_fault_tolerant import \
    UniversalHadamardFaultTolerant
from stim_experiments.error_correcting_codes.support.universal_hadamard.universal_hadamard_single_ancilla import \
    UniversalHadamardSingleAncilla
from stim_experiments.globals.error_correcting_code_configuration import ConfigurationErrorCorrectingCodeManager
from stim_experiments.globals.fresh_ancillas_pool import FreshAncillasPool
from stim_experiments.utilities.predefined_check_matrix_values import get_check_matrix_values_4_qubit, \
    get_check_matrix_values_5_qubit
from stim_experiments.utilities.utilities import KET_MINUS_STATE_VECTOR, KET_ONE_STATE_VECTOR, KET_PLUS_STATE_VECTOR, \
    KET_ZERO_STATE_VECTOR, \
    int_to_binary_array, states_are_equal, tensor
from tests.error_correcting_codes.support.universal_hadamard.universal_hadamard_fault_tolerant.double_qubit_double_logical_code import \
    DoubleQubitDoubleLogicalCode
from tests.utilities import set_configuration_to_reduce_ancilla_qubits


class TestUniversalHadamard:
    @pytest.fixture(autouse=True, params=range(5))
    def _seed(self, request):
        seed = 1
        random.seed(seed)
        np.random.seed(seed)
        ConfigurationErrorCorrectingCodeManager().get_configuration().seed = seed

    @pytest.fixture(autouse=True, params=[
        # pytest.param(UniversalHadamardSingleAncilla, id='UniversalHadamardSingleAncilla'),
        pytest.param(UniversalHadamardFaultTolerant, id='UniversalHadamardFaultTolerant'),
    ])
    def _setup(self, request, _seed):
        self._universal_hadamard_type: type[UniversalHadamard] = request.param

    def test_random_alpha_beta(self):
        code = RepetitionCode(num_qubits=1)
        universal_hadamard = self._universal_hadamard_type(code=code, qubit_index=0)
        FreshAncillasPool().set_first_ancilla_num(first_ancilla_num=len(code.data_qubits))

        initial_state = self._random_complex_unit_vector(num_qubits=1)
        utilities = get_error_correcting_code_utilities(state=initial_state)

        simulated_state = utilities.get_state_after_circuit(
            circuit=Circuit(
                code.encode_logical_qubit(),
                universal_hadamard.get_hadamard_circuit(),
            ),
            num_data_qubits=len(code.data_qubits),
            initial_data_state=initial_state,
        ).state
        expected_state = (1 / np.sqrt(2)) * array([initial_state[0] + initial_state[1], initial_state[0] - initial_state[1]])
        assert states_are_equal(simulated_state, expected_state)

    def test_multiple_qubit_encoding_hadamard_one_qubit(self):
        set_configuration_to_reduce_ancilla_qubits()
        code = StabilizerStandardizedCode(generators=get_check_matrix_values_4_qubit())
        universal_hadamard = self._universal_hadamard_type(code=code, qubit_index=1)
        FreshAncillasPool().set_first_ancilla_num(first_ancilla_num=len(code.data_qubits))

        initial_coefficients = self._random_complex_unit_vector(num_qubits=2)
        utilities = get_error_correcting_code_utilities(state=initial_coefficients)
        computational_basis_states = [int_to_binary_array(i, code.num_logical_qubits) for i in range(2 ** code.num_logical_qubits)]
        computational_basis_states_encoded = [
            utilities.get_state_after_circuit(
                circuit=Circuit(
                    code.encode_logical_qubit(),
                    [code.get_operation_circuit(LogicalOperation(gate=LogicalGateLabel.X, qubit_index=qubit_index))
                     for qubit_index, is_flipped in enumerate(basis_state)
                     if is_flipped],
                ),
                num_data_qubits=len(code.data_qubits),
            ).state
            for basis_state in computational_basis_states
        ]
        initial_state = sum(
            coefficient * computational_basis_state
            for coefficient, computational_basis_state in zip(initial_coefficients, computational_basis_states_encoded)
        )

        simulated_state = utilities.get_state_after_circuit(
            circuit=Circuit(
                code.encode_logical_qubit(),
                universal_hadamard.get_hadamard_circuit(),
            ),
            num_data_qubits=len(code.data_qubits),
            initial_data_state=initial_state,
        ).state

        expected_state = (
                (initial_coefficients[0] + initial_coefficients[1]) * computational_basis_states_encoded[0]
                + (initial_coefficients[0] - initial_coefficients[1]) * computational_basis_states_encoded[1]
                + (initial_coefficients[2] + initial_coefficients[3]) * computational_basis_states_encoded[2]
                + (initial_coefficients[2] - initial_coefficients[3]) * computational_basis_states_encoded[3]
        )
        assert states_are_equal(simulated_state, expected_state)

    @staticmethod
    def _random_complex_unit_vector(num_qubits: int) -> np.ndarray:
        dimension = 2 ** num_qubits
        random_complex_vector = np.random.randn(dimension) + 1j * np.random.randn(dimension)
        unit_complex_vector = random_complex_vector / np.linalg.norm(random_complex_vector)
        return unit_complex_vector
