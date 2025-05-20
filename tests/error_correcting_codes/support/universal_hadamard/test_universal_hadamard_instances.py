import numpy as np
import pytest
from cirq import Circuit
from numpy import array

from stim_experiments.error_correcting_codes.error_correcting_code_utilities import get_error_correcting_code_utilities
from stim_experiments.error_correcting_codes.repetition_code.repetition_code import RepetitionCode
from stim_experiments.error_correcting_codes.support.universal_hadamard.universal_hadamard import UniversalHadamard
from stim_experiments.error_correcting_codes.support.universal_hadamard.universal_hadamard_fault_tolerant import \
    UniversalHadamardFaultTolerant
from stim_experiments.error_correcting_codes.support.universal_hadamard.universal_hadamard_single_ancilla import \
    UniversalHadamardSingleAncilla
from stim_experiments.globals.fresh_ancillas_pool import FreshAncillasPool
from stim_experiments.utilities.utilities import KET_MINUS_STATE_VECTOR, KET_ONE_STATE_VECTOR, KET_PLUS_STATE_VECTOR, \
    KET_ZERO_STATE_VECTOR, \
    states_are_equal, tensor
from tests.error_correcting_codes.support.universal_hadamard.universal_hadamard_fault_tolerant.double_qubit_double_logical_code import \
    DoubleQubitDoubleLogicalCode
from tests.utilities import set_configuration_to_reduce_ancilla_qubits


class TestUniversalHadamard:
    @pytest.fixture(autouse=True, params=range(2))
    def _seed(self, request):
        np.random.seed(request.param)

    @pytest.fixture(autouse=True, params=[
        pytest.param(UniversalHadamardSingleAncilla, id='UniversalHadamardSingleAncilla'),
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
        code = DoubleQubitDoubleLogicalCode()
        universal_hadamard = self._universal_hadamard_type(code=code, qubit_index=1)
        FreshAncillasPool().set_first_ancilla_num(first_ancilla_num=len(code.data_qubits))

        initial_state = self._random_complex_unit_vector(num_qubits=2)
        utilities = get_error_correcting_code_utilities(state=initial_state)

        simulated_state = utilities.get_state_after_circuit(
            circuit=Circuit(
                code.encode_logical_qubit(),
                universal_hadamard.get_hadamard_circuit(),
            ),
            num_data_qubits=len(code.data_qubits),
            initial_data_state=initial_state,
        ).state
        expected_state = (initial_state[0] * tensor(KET_ZERO_STATE_VECTOR, KET_PLUS_STATE_VECTOR)
                          + initial_state[1] * tensor(KET_ZERO_STATE_VECTOR, KET_MINUS_STATE_VECTOR)
                          + initial_state[2] * tensor(KET_ONE_STATE_VECTOR, KET_PLUS_STATE_VECTOR)
                          + initial_state[3] * tensor(KET_ONE_STATE_VECTOR, KET_MINUS_STATE_VECTOR))
        assert states_are_equal(simulated_state, expected_state)

    @staticmethod
    def _random_complex_unit_vector(num_qubits: int) -> np.ndarray:
        dimension = 2 ** num_qubits
        random_complex_vector = np.random.randn(dimension) + 1j * np.random.randn(dimension)
        unit_complex_vector = random_complex_vector / np.linalg.norm(random_complex_vector)
        return unit_complex_vector
