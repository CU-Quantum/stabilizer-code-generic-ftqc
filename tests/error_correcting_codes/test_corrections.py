from dataclasses import dataclass

import pytest
from cirq import Circuit, Gate, LineQubit, X, Y, Z

from stim_experiments.error_correcting_codes.error_correcting_code.error_correcting_code import ErrorCorrectingCode
from stim_experiments.error_correcting_codes.error_correcting_code_utilities import get_error_correcting_code_utilities
from stim_experiments.error_correcting_codes.five_qubit_code.five_qubit_code import FiveQubitCode
from stim_experiments.error_correcting_codes.generic_stabilizer_code.generic_stabilizer_code import \
    GenericStabilizerCode
from stim_experiments.error_correcting_codes.shors_code.shors_repetition_code import ShorsRepetitionCode
from stim_experiments.error_correcting_codes.steane_code.staene_code import SteaneCode
from stim_experiments.error_correcting_codes.three_cat_code.three_cat_code import ThreeCatCode
from stim_experiments.utilities import FreshAncillasPool, KET_ZERO_DENSITY_MATRIX, KET_ZERO_STATE_VECTOR, \
    TYPE_STATE_VECTOR_OR_DENSITY_MATRIX, tensor
from tests.error_correcting_codes.five_qubit_code.expected_states_five_qubit import ExpectedStatesFiveQubit
from tests.error_correcting_codes.generic_stabilizer_code.expected_states_generic_5_qubit import \
    ExpectedStatesGenericFiveQubit
from tests.error_correcting_codes.generic_stabilizer_code.utilities import get_check_matrix_values_5_qubit
from tests.error_correcting_codes.shors_code.expected_states_shor import ExpectedStatesShor
from tests.error_correcting_codes.steane_code.expected_states_steane import ExpectedStatesSteane
from tests.error_correcting_codes.three_cat_code.expected_states_three_cat import ExpectedStatesThreeCat
from tests.utilities import states_are_equal

QUBIT_INDICES_IN_DIFFERENT_POSITIONS_IN_DIFFERENT_SHOR_BLOCKS = [0, 4, 8]
ARBITRARY_QUBIT_INDICES = [0, 2, 6]


@dataclass
class ParametersForCorrectionsTest:
    code: ErrorCorrectingCode
    expected_state: TYPE_STATE_VECTOR_OR_DENSITY_MATRIX
    initial_state: TYPE_STATE_VECTOR_OR_DENSITY_MATRIX
    qubit_indices_to_test: list[int]


PARAMETERS = {
    "ThreeCatCode": ParametersForCorrectionsTest(
        code=ThreeCatCode(num_qubits_in_cat_state=ExpectedStatesThreeCat().arbitrary_num_qubits),
        expected_state=ExpectedStatesThreeCat().get_logical_zero_state_vector(),
        initial_state=tensor(*[KET_ZERO_STATE_VECTOR] * ExpectedStatesThreeCat().arbitrary_num_qubits * ThreeCatCode.num_cats),
        qubit_indices_to_test=list(range(0,
                                         ExpectedStatesThreeCat().arbitrary_num_qubits * ThreeCatCode.num_cats,
                                         ExpectedStatesThreeCat().arbitrary_num_qubits + 1)),
    ),
    "GenericStabilizerCodeFiveQubit": ParametersForCorrectionsTest(
        code=GenericStabilizerCode(generators=get_check_matrix_values_5_qubit()),
        expected_state=ExpectedStatesGenericFiveQubit().get_logical_zero_state_vector(),
        initial_state=tensor(*[KET_ZERO_STATE_VECTOR] * 5),
        qubit_indices_to_test=list(range(5)),
    ),
    "FiveQubitCode": ParametersForCorrectionsTest(
        code=FiveQubitCode(),
        expected_state=ExpectedStatesFiveQubit().get_logical_zero_state_vector(),
        initial_state=tensor(*[KET_ZERO_STATE_VECTOR] * 5),
        qubit_indices_to_test=list(range(5)),
    ),
    "SteaneCode": ParametersForCorrectionsTest(
        code=SteaneCode(),
        expected_state=ExpectedStatesSteane().get_logical_zero_state_vector(),
        initial_state=tensor(*[KET_ZERO_STATE_VECTOR] * 7),
        qubit_indices_to_test=ARBITRARY_QUBIT_INDICES
    ),
    "ShorsRepetitionCode": ParametersForCorrectionsTest(
        code=ShorsRepetitionCode(),
        expected_state=ExpectedStatesShor().get_logical_zero_density_matrix(),
        initial_state=tensor(*[KET_ZERO_DENSITY_MATRIX] * 9),
        qubit_indices_to_test=QUBIT_INDICES_IN_DIFFERENT_POSITIONS_IN_DIFFERENT_SHOR_BLOCKS
    ),
}


PARAMETERS_FLATTENED = [pytest.param((parameters, qubit_index), id=f'{name}_qubit-{qubit_index}')
                        for name, parameters in PARAMETERS.items() for qubit_index in parameters.qubit_indices_to_test]


class TestCorrections:
    @pytest.fixture(autouse=True, params=PARAMETERS_FLATTENED)
    def _setup(self, request):
        self._parameters: ParametersForCorrectionsTest = request.param[0]
        self._qubit_index: int = request.param[1]
        FreshAncillasPool().set_first_ancilla_num(first_ancilla_num=len(self._parameters.code.data_qubits))

    def test_bit_flip_error_is_corrected(self):
        self._error_is_corrected(error_gate=X, qubit_index=self._qubit_index)

    def test_phase_flip_error_is_corrected(self):
        self._error_is_corrected(error_gate=Z, qubit_index=self._qubit_index)

    def test_pauli_y_error_is_corrected(self):
        self._error_is_corrected(error_gate=Y, qubit_index=self._qubit_index)

    def _error_is_corrected(self, error_gate: Gate, qubit_index: int) -> None:
        circuit = Circuit(
            self._parameters.code.encode_logical_qubit(),
            error_gate(LineQubit(qubit_index)),
            self._parameters.code.get_error_correction_circuit(),
        )

        utilities = get_error_correcting_code_utilities(state=self._parameters.initial_state)
        simulation_state = utilities.get_state_after_circuit(circuit=circuit,
                                                             num_data_qubits=len(self._parameters.code.data_qubits),
                                                             initial_data_state=self._parameters.initial_state,
                                                             )
        assert states_are_equal(simulation_state.state, self._parameters.expected_state)
