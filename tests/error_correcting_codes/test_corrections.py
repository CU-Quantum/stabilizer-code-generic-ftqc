from dataclasses import dataclass

import numpy
import pytest
from cirq import Circuit, Gate, LineQubit, X, Y, Z

from stim_experiments.error_correcting_codes.error_correcting_code.error_correcting_code import ErrorCorrectingCode
from stim_experiments.error_correcting_codes.error_correcting_code_utilities import get_error_correcting_code_utilities
from stim_experiments.error_correcting_codes.five_qubit_code.five_qubit_code import FiveQubitCode
from stim_experiments.error_correcting_codes.repetition_code.repetition_code import RepetitionCode
from stim_experiments.error_correcting_codes.stabilizer_standardized_code.stabilizer_standardized_code import \
    StabilizerStandardizedCode
from stim_experiments.error_correcting_codes.shors_code.shors_repetition_code import ShorsRepetitionCode
from stim_experiments.error_correcting_codes.steane_code.staene_code import SteaneCode
from stim_experiments.error_correcting_codes.three_cat_code.three_cat_code import ThreeCatCode
from stim_experiments.error_correcting_codes.cat_parity_code.cat_parity_code import \
    CatParityCode
from stim_experiments.error_correcting_codes.universal_hadamard_helper_code.universal_hadamard_helper_code import \
    UniversalHadamardHelperCode
from stim_experiments.globals.fresh_ancillas_pool import FreshAncillasPool
from stim_experiments.utilities.utilities import TYPE_STATE_VECTOR_OR_DENSITY_MATRIX, states_are_equal
from tests.error_correcting_codes.five_qubit_code.expected_states_five_qubit import ExpectedStatesFiveQubit
from tests.error_correcting_codes.stabilizer_standardized_code.expected_states_standardized_5_qubit import \
    ExpectedStatesGenericFiveQubit
from stim_experiments.utilities.predefined_check_matrix_values import get_check_matrix_values_5_qubit
from tests.error_correcting_codes.repetition_code.expected_states_repetition import ExpectedStatesRepetition
from tests.error_correcting_codes.shors_code.expected_states_shor import ExpectedStatesShor
from tests.error_correcting_codes.steane_code.expected_states_steane import ExpectedStatesSteane
from tests.error_correcting_codes.three_cat_code.expected_states_three_cat import ExpectedStatesThreeCat
from tests.error_correcting_codes.cat_parity_code.expected_states_cat_parity import \
    ExpectedStatesCatParity
from tests.error_correcting_codes.universal_hadamard_helper_code.expected_states_universal_hadamard_helper import \
    ExpectedStatesUniversalHadamardHelper
from tests.utilities import set_configuration_to_reduce_ancilla_qubits

QUBIT_INDICES_IN_DIFFERENT_POSITIONS_IN_DIFFERENT_SHOR_BLOCKS = [0, 4, 8]
ARBITRARY_QUBIT_INDICES = [0, 2, 6]
QUBIT_INDICES_IN_DIFFERENT_POSITIONS_IN_DIFFERENT_UNIVERSAL_HADAMARD_BLOCKS = list(
    range(0,
          ExpectedStatesCatParity().num_qubits * CatParityCode.num_cats,
          ExpectedStatesCatParity().num_qubits + 2,
          )) + [ExpectedStatesCatParity().num_qubits * CatParityCode.num_cats - 1]


@dataclass
class ParametersForCorrectionsTest:
    code: ErrorCorrectingCode
    initial_state: TYPE_STATE_VECTOR_OR_DENSITY_MATRIX
    qubit_indices_to_test: list[int]


PARAMETERS = {
    "UniversalHadamardHelperCode": ParametersForCorrectionsTest(
        code=UniversalHadamardHelperCode(num_qubits_in_cat_state=ExpectedStatesUniversalHadamardHelper().num_qubits),
        initial_state=ExpectedStatesUniversalHadamardHelper().get_logical_zero_state_vector(),
        qubit_indices_to_test=list(range(ExpectedStatesUniversalHadamardHelper().num_qubits, ExpectedStatesUniversalHadamardHelper().num_qubits * 3)),
    ),
    "RepetitionCode": ParametersForCorrectionsTest(
        code=RepetitionCode(num_qubits=ExpectedStatesRepetition().arbitrary_num_qubits),
        initial_state=ExpectedStatesRepetition().get_logical_zero_state_vector(),
        qubit_indices_to_test=list(range(3)),
    ),
    "CatParityCodeZeroState": ParametersForCorrectionsTest(
        code=CatParityCode(num_qubits_in_cat_state=ExpectedStatesCatParity().num_qubits),
        initial_state=ExpectedStatesCatParity().get_logical_zero_state_vector(),
        qubit_indices_to_test=QUBIT_INDICES_IN_DIFFERENT_POSITIONS_IN_DIFFERENT_UNIVERSAL_HADAMARD_BLOCKS
    ),
    "CatParityCodeOneState": ParametersForCorrectionsTest(
        code=CatParityCode(num_qubits_in_cat_state=ExpectedStatesCatParity().num_qubits),
        initial_state=ExpectedStatesCatParity().get_logical_one_state_vector(),
        qubit_indices_to_test=QUBIT_INDICES_IN_DIFFERENT_POSITIONS_IN_DIFFERENT_UNIVERSAL_HADAMARD_BLOCKS
    ),
    "ThreeCatCode": ParametersForCorrectionsTest(
        code=ThreeCatCode(num_qubits_in_cat_state=ExpectedStatesThreeCat().arbitrary_num_qubits),
        initial_state=ExpectedStatesThreeCat().get_logical_zero_state_vector(),
        qubit_indices_to_test=list(range(0,
                                         ExpectedStatesThreeCat().arbitrary_num_qubits * ThreeCatCode.num_cats,
                                         ExpectedStatesThreeCat().arbitrary_num_qubits + 2)) + [ExpectedStatesThreeCat().arbitrary_num_qubits * ThreeCatCode.num_cats - 1],
    ),
    "GenericStabilizerCodeFiveQubit": ParametersForCorrectionsTest(
        code=StabilizerStandardizedCode(generators=get_check_matrix_values_5_qubit()),
        initial_state=ExpectedStatesGenericFiveQubit().get_logical_zero_state_vector(),
        qubit_indices_to_test=list(range(5)),
    ),
    "FiveQubitCode": ParametersForCorrectionsTest(
        code=FiveQubitCode(),
        initial_state=ExpectedStatesFiveQubit().get_logical_zero_state_vector(),
        qubit_indices_to_test=list(range(5)),
    ),
    "SteaneCode": ParametersForCorrectionsTest(
        code=SteaneCode(),
        initial_state=ExpectedStatesSteane().get_logical_zero_state_vector(),
        qubit_indices_to_test=ARBITRARY_QUBIT_INDICES
    ),
    "ShorsRepetitionCode": ParametersForCorrectionsTest(
        code=ShorsRepetitionCode(),
        initial_state=ExpectedStatesShor().get_logical_zero_state_vector(),
        qubit_indices_to_test=QUBIT_INDICES_IN_DIFFERENT_POSITIONS_IN_DIFFERENT_SHOR_BLOCKS
    ),
}


PARAMETERS_FLATTENED = [pytest.param((parameters, qubit_index), id=f'{name}_qubit-{qubit_index}')
                        for name, parameters in PARAMETERS.items() for qubit_index in parameters.qubit_indices_to_test]


class TestCorrections:
    @pytest.fixture(autouse=True, params=PARAMETERS_FLATTENED)
    def _setup(self, request):
        numpy.random.seed(0)
        self._parameters: ParametersForCorrectionsTest = request.param[0]
        self._qubit_index: int = request.param[1]
        FreshAncillasPool().set_first_ancilla_num(first_ancilla_num=len(self._parameters.code.data_qubits))
        set_configuration_to_reduce_ancilla_qubits()

    def test_bit_flip_error_is_corrected(self):
        self._error_is_corrected(error_gate=X, qubit_index=self._qubit_index)

    def test_phase_flip_error_is_corrected(self):
        self._error_is_corrected(error_gate=Z, qubit_index=self._qubit_index)

    def test_pauli_y_error_is_corrected(self):
        self._error_is_corrected(error_gate=Y, qubit_index=self._qubit_index)

    def _error_is_corrected(self, error_gate: Gate, qubit_index: int) -> None:
        utilities = get_error_correcting_code_utilities(state=self._parameters.initial_state)
        simulation_state = utilities.get_state_after_circuit(
            circuit=Circuit(
                error_gate(LineQubit(qubit_index)),
                self._parameters.code.get_error_correction_circuit(),
            ),
            num_data_qubits=len(self._parameters.code.data_qubits),
            initial_data_state=self._parameters.initial_state,
        ).state
        assert states_are_equal(simulation_state, self._parameters.initial_state)
