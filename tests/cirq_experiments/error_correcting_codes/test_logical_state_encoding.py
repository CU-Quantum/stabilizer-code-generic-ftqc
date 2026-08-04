from dataclasses import dataclass

import pytest

from cirq_experiments.error_correcting_codes.error_correcting_code.error_correcting_code import ErrorCorrectingCode
from cirq_experiments.error_correcting_codes.five_qubit_code.five_qubit_code import FiveQubitCode
from cirq_experiments.error_correcting_codes.repetition_code.repetition_code import RepetitionCodeOneLogical
from cirq_experiments.error_correcting_codes.stabilizer_standardized_code.stabilizer_standardized_code import \
    StabilizerStandardizedCode
from cirq_experiments.error_correcting_codes.shors_code.shors_repetition_code import ShorsRepetitionCode
from cirq_experiments.error_correcting_codes.steane_code.staene_code import SteaneCode
from cirq_experiments.error_correcting_codes.generalized_shor_code_hadamard.generalized_shor_code_hadamard import \
    GeneralizedShorCodeHadamard

from cirq_experiments.error_correcting_codes.generalized_shor_code.generalized_shor_code import GeneralizedShorCode
from cirq_experiments.globals.fresh_ancillas_pool import FreshAncillasPool
from cirq_experiments.simulations.error_correcting_simulator import get_error_correcting_simulator
from cirq_experiments.utilities.utilities import KET_ONE_DENSITY_MATRIX, KET_ONE_STATE_VECTOR, KET_ZERO_DENSITY_MATRIX, \
    KET_ZERO_STATE_VECTOR, \
    TYPE_STATE_VECTOR_OR_DENSITY_MATRIX, states_are_equal, tensor
from tests.cirq_experiments.error_correcting_codes.five_qubit_code.expected_states_five_qubit import ExpectedStatesFiveQubit
from tests.cirq_experiments.error_correcting_codes.generalized_shor_code.expected_states_generalized_shor import ExpectedStatesGeneralizedShor
from tests.cirq_experiments.error_correcting_codes.stabilizer_standardized_code.expected_states_standardized_5_qubit import \
    ExpectedStatesGenericFiveQubit
from tests.cirq_experiments.error_correcting_codes.stabilizer_standardized_code.expected_states_standardized_golay import \
    ExpectedStatesGenericGolay
from tests.cirq_experiments.error_correcting_codes.stabilizer_standardized_code.expected_states_standardized_steane import \
    ExpectedStatesGenericSteane
from predefined_check_matrix_values import get_check_matrix_values_5_qubit, \
    get_check_matrix_values_golay, get_check_matrix_values_steane
from tests.cirq_experiments.error_correcting_codes.repetition_code.expected_states_repetition import ExpectedStatesRepetition
from tests.cirq_experiments.error_correcting_codes.shors_code.expected_states_shor import ExpectedStatesShor
from tests.cirq_experiments.error_correcting_codes.steane_code.expected_states_steane import ExpectedStatesSteane
from tests.cirq_experiments.error_correcting_codes.generalized_shor_code_hadamard.expected_states_generalized_shor_hadamard import \
    ExpectedStatesGeneralizedShorHadamard
from tests.cirq_experiments.utilities_for_tests import set_configuration_to_reduce_ancilla_qubits


@dataclass
class ParametersForStateEncodingTest:
    code: ErrorCorrectingCode
    expected_state: TYPE_STATE_VECTOR_OR_DENSITY_MATRIX
    initial_data_state: TYPE_STATE_VECTOR_OR_DENSITY_MATRIX


@dataclass
class StateParameters:
    zero: ParametersForStateEncodingTest
    one: ParametersForStateEncodingTest


PARAMETERS = {
    "MultipleCatCode": StateParameters(
        zero=ParametersForStateEncodingTest(
            code=GeneralizedShorCode(num_cats=ExpectedStatesGeneralizedShor().arbitrary_num_cats,
                                     num_qubits_per_cat=ExpectedStatesGeneralizedShor().arbitrary_num_qubits_per_cat),
            expected_state=ExpectedStatesGeneralizedShor().get_logical_zero_state_vector(),
            initial_data_state=tensor(*[KET_ZERO_STATE_VECTOR] * ExpectedStatesGeneralizedShor().arbitrary_num_qubits_per_cat * ExpectedStatesGeneralizedShor().arbitrary_num_cats),
        ),
        one=ParametersForStateEncodingTest(
            code=GeneralizedShorCode(num_cats=ExpectedStatesGeneralizedShor().arbitrary_num_cats,
                                     num_qubits_per_cat=ExpectedStatesGeneralizedShor().arbitrary_num_qubits_per_cat),
            expected_state=ExpectedStatesGeneralizedShor().get_logical_one_state_vector(),
            initial_data_state=tensor(*[tensor(KET_ONE_STATE_VECTOR, *[KET_ZERO_STATE_VECTOR] * (ExpectedStatesGeneralizedShor().arbitrary_num_qubits_per_cat - 1))] * ExpectedStatesGeneralizedShor().arbitrary_num_cats),
        ),
    ),
    "RepetitionCode": StateParameters(
        zero=ParametersForStateEncodingTest(
            code=RepetitionCodeOneLogical(num_qubits=ExpectedStatesRepetition().arbitrary_num_qubits),
            expected_state=ExpectedStatesRepetition().get_logical_zero_density_matrix(),
            initial_data_state=tensor(*[KET_ZERO_DENSITY_MATRIX] * ExpectedStatesRepetition().arbitrary_num_qubits),
        ),
        one=ParametersForStateEncodingTest(
            code=RepetitionCodeOneLogical(num_qubits=ExpectedStatesRepetition().arbitrary_num_qubits),
            expected_state=ExpectedStatesRepetition().get_logical_one_density_matrix(),
            initial_data_state=tensor(*[KET_ONE_DENSITY_MATRIX] * ExpectedStatesRepetition().arbitrary_num_qubits),
        ),
    ),
    "CatParityCode": StateParameters(
        zero=ParametersForStateEncodingTest(
            code=GeneralizedShorCodeHadamard(num_cats=ExpectedStatesGeneralizedShorHadamard().num_cats, num_qubits_per_cat=ExpectedStatesGeneralizedShorHadamard().num_qubits_per_cat),
            expected_state=ExpectedStatesGeneralizedShorHadamard().get_logical_zero_state_vector(),
            initial_data_state=tensor(*[KET_ZERO_STATE_VECTOR] * ExpectedStatesGeneralizedShorHadamard().num_qubits_per_cat * ExpectedStatesGeneralizedShorHadamard().num_cats),
        ),
        one=ParametersForStateEncodingTest(
            code=GeneralizedShorCodeHadamard(num_cats=ExpectedStatesGeneralizedShorHadamard().num_cats, num_qubits_per_cat=ExpectedStatesGeneralizedShorHadamard().num_qubits_per_cat),
            expected_state=ExpectedStatesGeneralizedShorHadamard().get_logical_one_state_vector(),
            initial_data_state=tensor(*[KET_ONE_STATE_VECTOR] * ExpectedStatesGeneralizedShorHadamard().num_qubits_per_cat * ExpectedStatesGeneralizedShorHadamard().num_cats),
        ),
    ),
    "GenericStabilizerCodeFiveQubit": StateParameters(
        zero=ParametersForStateEncodingTest(
            code=StabilizerStandardizedCode(generators=get_check_matrix_values_5_qubit()),
            expected_state=ExpectedStatesGenericFiveQubit().get_logical_zero_state_vector(),
            initial_data_state=tensor(*[KET_ZERO_STATE_VECTOR] * 5),
        ),
        one=ParametersForStateEncodingTest(
            code=StabilizerStandardizedCode(generators=get_check_matrix_values_5_qubit()),
            expected_state=ExpectedStatesGenericFiveQubit().get_logical_one_state_vector(),
            initial_data_state=tensor(*[KET_ZERO_STATE_VECTOR] * 4, KET_ONE_STATE_VECTOR),
        ),
    ),
    "GenericStabilizerCodeStaeneCode": StateParameters(
        zero=ParametersForStateEncodingTest(
            code=StabilizerStandardizedCode(generators=get_check_matrix_values_steane()),
            expected_state=ExpectedStatesGenericSteane().get_logical_zero_state_vector(),
            initial_data_state=tensor(*[KET_ZERO_STATE_VECTOR] * 7),
        ),
        one=ParametersForStateEncodingTest(
            code=StabilizerStandardizedCode(generators=get_check_matrix_values_steane()),
            expected_state=ExpectedStatesGenericSteane().get_logical_one_state_vector(),
            initial_data_state=tensor(*[KET_ZERO_STATE_VECTOR] * 6, KET_ONE_STATE_VECTOR),
        ),
    ),
    "GenericStabilizerCodeGolay": StateParameters(
        zero=ParametersForStateEncodingTest(
            code=StabilizerStandardizedCode(generators=get_check_matrix_values_golay()),
            expected_state=ExpectedStatesGenericGolay().get_logical_zero_state_vector(),
            initial_data_state=tensor(*[KET_ZERO_STATE_VECTOR] * 23),
        ),
        one=ParametersForStateEncodingTest(
            code=StabilizerStandardizedCode(generators=get_check_matrix_values_golay()),
            expected_state=ExpectedStatesGenericGolay().get_logical_one_state_vector(),
            initial_data_state=tensor(*[KET_ZERO_STATE_VECTOR] * 22, KET_ONE_STATE_VECTOR),
        ),
    ),
    "FiveQubitCode": StateParameters(
        zero=ParametersForStateEncodingTest(
            code=FiveQubitCode(),
            expected_state=ExpectedStatesFiveQubit().get_logical_zero_state_vector(),
            initial_data_state=tensor(*[KET_ZERO_STATE_VECTOR] * 5),
        ),
        one=ParametersForStateEncodingTest(
            code=FiveQubitCode(),
            expected_state=ExpectedStatesFiveQubit().get_logical_one_state_vector(),
            initial_data_state=tensor(*[KET_ONE_STATE_VECTOR] * 5),
        ),
    ),
    "SteaneCode": StateParameters(
        zero=ParametersForStateEncodingTest(
            code=SteaneCode(),
            expected_state=ExpectedStatesSteane().get_logical_zero_density_matrix(),
            initial_data_state=tensor(*[KET_ZERO_DENSITY_MATRIX] * 7),
        ),
        one=ParametersForStateEncodingTest(
            code=SteaneCode(),
            expected_state=ExpectedStatesSteane().get_logical_one_density_matrix(),
            initial_data_state=tensor(*[KET_ONE_DENSITY_MATRIX] * 7),
        ),
    ),
    "ShorsRepetitionCode": StateParameters(
        zero=ParametersForStateEncodingTest(
            code=ShorsRepetitionCode(),
            expected_state=ExpectedStatesShor().get_logical_zero_density_matrix(),
            initial_data_state=tensor(*[KET_ZERO_DENSITY_MATRIX] * 9),
        ),
        one=ParametersForStateEncodingTest(
            code=ShorsRepetitionCode(),
            expected_state=ExpectedStatesShor().get_logical_one_density_matrix(),
            initial_data_state=tensor(*[tensor(KET_ONE_DENSITY_MATRIX, *[KET_ZERO_DENSITY_MATRIX] * 2)] * 3),
        ),
    ),
}


PARAMETERS_FLATTENED = [pytest.param(parameters, id=f'{name}_state-{i}')
                        for name, states in PARAMETERS.items() for i, parameters in enumerate((states.zero, states.one))]


class TestLogicalStateEncoding:
    @pytest.fixture(autouse=True, params=PARAMETERS_FLATTENED)
    def _setup(self, request):
        self._parameters: ParametersForStateEncodingTest = request.param
        FreshAncillasPool().set_first_ancilla_num(first_ancilla_num=len(self._parameters.code.data_qubits))
        set_configuration_to_reduce_ancilla_qubits()

    def test_encoding(self):
        encoding = self._parameters.code.encode_logical_qubit()
        utilities = get_error_correcting_simulator(state=self._parameters.initial_data_state)
        data_state = utilities.run_simulation(circuit=encoding,
                                              num_data_qubits=len(self._parameters.code.data_qubits),
                                              initial_data_state=self._parameters.initial_data_state).state
        assert states_are_equal(data_state, self._parameters.expected_state)
