import numpy as np
from cirq import Circuit, LineQubit
from numpy import array

from stim_experiments.error_correcting_codes.error_correcting_code_utilities import get_error_correcting_code_utilities
from stim_experiments.error_correcting_codes.support.universal_hadamard.universal_hadamard import UniversalHadamard
from stim_experiments.globals.fresh_ancillas_pool import FreshAncillasPool
from tests.error_correcting_codes.support.universal_hadamard.single_qubit_code import SingleQubitCode
from tests.utilities import states_are_equal


class TestUniversalHadamard:
    def test_random_alpha_beta(self):
        np.random.seed(0)
        initial_state = self._random_complex_unit_vector()
        utilities = get_error_correcting_code_utilities(state=initial_state)
        qubits = LineQubit.range(1)
        code = SingleQubitCode(qubits=qubits)
        FreshAncillasPool().set_first_ancilla_num(first_ancilla_num=len(code.data_qubits))

        simulated_state = utilities.get_state_after_circuit(
            circuit=Circuit(
                code.encode_logical_qubit(),
                UniversalHadamard(code=code).get_hadamard_circuit(),
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
