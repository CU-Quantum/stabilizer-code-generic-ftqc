from dataclasses import dataclass

import numpy
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
from stim_experiments.error_correcting_codes.three_cat_subregister_parity_code.three_cat_subregister_parity_code import \
    ThreeCatSubregisterParityCode
from stim_experiments.globals.fresh_ancillas_pool import FreshAncillasPool
from stim_experiments.utilities.utilities import TYPE_STATE_VECTOR_OR_DENSITY_MATRIX
from tests.error_correcting_codes.five_qubit_code.expected_states_five_qubit import ExpectedStatesFiveQubit
from tests.error_correcting_codes.generic_stabilizer_code.expected_states_generic_5_qubit import \
    ExpectedStatesGenericFiveQubit
from stim_experiments.utilities.predefined_check_matrix_values import get_check_matrix_values_5_qubit
from tests.error_correcting_codes.shors_code.expected_states_shor import ExpectedStatesShor
from tests.error_correcting_codes.steane_code.expected_states_steane import ExpectedStatesSteane
from tests.error_correcting_codes.three_cat_code.expected_states_three_cat import ExpectedStatesThreeCat
from tests.error_correcting_codes.universal_hadamard_code.expected_states_universal_hadamard import \
    ExpectedStatesThreeCatSubregisterParity
from tests.utilities import set_configuration_to_reduce_ancilla_qubits, states_are_equal

QUBIT_INDICES_IN_DIFFERENT_POSITIONS_IN_DIFFERENT_SHOR_BLOCKS = [0, 4, 8]
ARBITRARY_QUBIT_INDICES = [0, 2, 6]
QUBIT_INDICES_IN_DIFFERENT_POSITIONS_IN_DIFFERENT_UNIVERSAL_HADAMARD_BLOCKS = list(
    range(0,
          ExpectedStatesThreeCatSubregisterParity().arbitrary_num_qubits * ThreeCatSubregisterParityCode.num_cats,
          ExpectedStatesThreeCatSubregisterParity().arbitrary_num_qubits + 2,
          )) + [ExpectedStatesThreeCatSubregisterParity().arbitrary_num_qubits * ThreeCatSubregisterParityCode.num_cats - 1]


@dataclass
class ParametersForCorrectionsTest:
    code: ErrorCorrectingCode
    initial_state: TYPE_STATE_VECTOR_OR_DENSITY_MATRIX
    qubit_indices_to_test: list[int]


PARAMETERS = {
    "ThreeCatSubregisterParityZeroState": ParametersForCorrectionsTest(
        code=ThreeCatSubregisterParityCode(num_qubits_in_cat_state=ExpectedStatesThreeCatSubregisterParity().arbitrary_num_qubits),
        initial_state=ExpectedStatesThreeCatSubregisterParity().get_logical_zero_state_vector(),
        qubit_indices_to_test=QUBIT_INDICES_IN_DIFFERENT_POSITIONS_IN_DIFFERENT_UNIVERSAL_HADAMARD_BLOCKS
    ),
    "ThreeCatSubregisterParityOneState": ParametersForCorrectionsTest(
        code=ThreeCatSubregisterParityCode(num_qubits_in_cat_state=ExpectedStatesThreeCatSubregisterParity().arbitrary_num_qubits),
        initial_state=ExpectedStatesThreeCatSubregisterParity().get_logical_one_state_vector(),
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
        code=GenericStabilizerCode(generators=get_check_matrix_values_5_qubit()),
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
