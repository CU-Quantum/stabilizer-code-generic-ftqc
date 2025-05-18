import numpy as np
import pytest
from cirq import Circuit, LineQubit
from numpy import array

from stim_experiments.error_correcting_codes.error_correcting_code_utilities import get_error_correcting_code_utilities
from stim_experiments.error_correcting_codes.support.universal_hadamard.universal_hadamard import UniversalHadamard
from stim_experiments.error_correcting_codes.support.universal_hadamard.universal_hadamard_fault_tolerant.universal_hadamard_fault_tolerant import \
    UniversalHadamardFaultTolerant
from stim_experiments.error_correcting_codes.support.universal_hadamard.universal_hadamard_single_ancilla import \
    UniversalHadamardSingleAncilla
from stim_experiments.globals.fresh_ancillas_pool import FreshAncillasPool
from tests.error_correcting_codes.support.universal_hadamard.universal_hadamard_fault_tolerant.single_qubit_code import SingleQubitCode
from stim_experiments.utilities.utilities import states_are_equal


class TestUniversalHadamard:
    @pytest.fixture(autouse=True, params=[
        pytest.param(UniversalHadamardSingleAncilla, id='UniversalHadamardSingleAncilla'),
        pytest.param(UniversalHadamardFaultTolerant, id='UniversalHadamardFaultTolerant'),
    ])
    def _setup(self, request):
        qubits = LineQubit.range(1)
        self._code = SingleQubitCode(qubits=qubits)
        universal_hadamard_type: type[UniversalHadamard] = request.param
        self._universal_hadamard = universal_hadamard_type(code=self._code, qubit_index=0)
        FreshAncillasPool().set_first_ancilla_num(first_ancilla_num=len(self._code.data_qubits))

    def test_random_alpha_beta(self):
        np.random.seed(0)
        initial_state = self._random_complex_unit_vector()
        utilities = get_error_correcting_code_utilities(state=initial_state)

        simulated_state = utilities.get_state_after_circuit(
            circuit=Circuit(
                self._code.encode_logical_qubit(),
                self._universal_hadamard.get_hadamard_circuit(),
            ),
            num_data_qubits=1,
            initial_data_state=initial_state,
        ).state
        expected_state = (1 / np.sqrt(2)) * array([initial_state[0] + initial_state[1], initial_state[0] - initial_state[1]])
        assert states_are_equal(simulated_state, expected_state)

    @staticmethod
    def _random_complex_unit_vector() -> np.ndarray:
        dimension = 2
        random_complex_vector = np.random.randn(dimension) + 1j * np.random.randn(dimension)
        unit_complex_vector = random_complex_vector / np.linalg.norm(random_complex_vector)
        return unit_complex_vector
