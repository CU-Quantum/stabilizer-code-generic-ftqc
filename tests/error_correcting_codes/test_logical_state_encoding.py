from dataclasses import dataclass

import pytest

from stim_experiments.error_correcting_codes.error_correcting_code.error_correcting_code import ErrorCorrectingCode
from stim_experiments.error_correcting_codes.error_correcting_code_utilities import \
    get_error_correcting_code_utilities
from stim_experiments.error_correcting_codes.five_qubit_code.five_qubit_code import FiveQubitCode
from stim_experiments.error_correcting_codes.generic_stabilizer_code.generic_stabilizer_code import \
    GenericStabilizerCode
from stim_experiments.error_correcting_codes.shors_code.shors_repetition_code import ShorsRepetitionCode
from stim_experiments.error_correcting_codes.steane_code.staene_code import SteaneCode
from stim_experiments.error_correcting_codes.three_cat_code.three_cat_code import ThreeCatCode
from stim_experiments.error_correcting_codes.three_cat_subregister_parity_code.three_cat_subregister_parity_code import \
    ThreeCatSubregisterParityCode
from stim_experiments.globals.fresh_ancillas_pool import FreshAncillasPool
from stim_experiments.utilities import KET_ONE_DENSITY_MATRIX, KET_ONE_STATE_VECTOR, \
    KET_ZERO_DENSITY_MATRIX, \
    KET_ZERO_STATE_VECTOR, TYPE_STATE_VECTOR_OR_DENSITY_MATRIX, tensor
from tests.error_correcting_codes.five_qubit_code.expected_states_five_qubit import ExpectedStatesFiveQubit
from tests.error_correcting_codes.generic_stabilizer_code.expected_states_generic_5_qubit import \
    ExpectedStatesGenericFiveQubit
from tests.error_correcting_codes.generic_stabilizer_code.expected_states_generic_steane import \
    ExpectedStatesGenericSteane
from tests.error_correcting_codes.generic_stabilizer_code.utilities import get_check_matrix_values_5_qubit, \
    get_check_matrix_values_steane
from tests.error_correcting_codes.shors_code.expected_states_shor import ExpectedStatesShor
from tests.error_correcting_codes.steane_code.expected_states_steane import ExpectedStatesSteane
from tests.error_correcting_codes.three_cat_code.expected_states_three_cat import ExpectedStatesThreeCat
from tests.error_correcting_codes.universal_hadamard_code.expected_states_universal_hadamard import \
    ExpectedStatesUniversalHadamard
from tests.utilities import states_are_equal


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
    "UniversalHadamardCode": StateParameters(
        zero=ParametersForStateEncodingTest(
            code=ThreeCatSubregisterParityCode(num_qubits_in_cat_state=ExpectedStatesUniversalHadamard().arbitrary_num_qubits),
            expected_state=ExpectedStatesUniversalHadamard().get_logical_zero_state_vector(),
            initial_data_state=tensor(*[KET_ZERO_STATE_VECTOR] * ExpectedStatesUniversalHadamard().arbitrary_num_qubits * ThreeCatCode.num_cats),
        ),
        one=ParametersForStateEncodingTest(
            code=ThreeCatSubregisterParityCode(num_qubits_in_cat_state=ExpectedStatesUniversalHadamard().arbitrary_num_qubits),
            expected_state=ExpectedStatesUniversalHadamard().get_logical_one_state_vector(),
            initial_data_state=tensor(*[KET_ONE_STATE_VECTOR] * ExpectedStatesUniversalHadamard().arbitrary_num_qubits * ThreeCatCode.num_cats),
        ),
    ),
    "ThreeCatCode": StateParameters(
        zero=ParametersForStateEncodingTest(
            code=ThreeCatCode(num_qubits_in_cat_state=ExpectedStatesThreeCat().arbitrary_num_qubits),
            expected_state=ExpectedStatesThreeCat().get_logical_zero_state_vector(),
            initial_data_state=tensor(*[KET_ZERO_STATE_VECTOR] * ExpectedStatesThreeCat().arbitrary_num_qubits * ThreeCatCode.num_cats),
        ),
        one=ParametersForStateEncodingTest(
            code=ThreeCatCode(num_qubits_in_cat_state=ExpectedStatesThreeCat().arbitrary_num_qubits),
            expected_state=ExpectedStatesThreeCat().get_logical_one_state_vector(),
            initial_data_state=tensor(*[tensor(KET_ONE_STATE_VECTOR, *[KET_ZERO_STATE_VECTOR] * (ExpectedStatesThreeCat().arbitrary_num_qubits - 1))] * ThreeCatCode.num_cats),
        ),
    ),
    "GenericStabilizerCodeFiveQubit": StateParameters(
        zero=ParametersForStateEncodingTest(
            code=GenericStabilizerCode(generators=get_check_matrix_values_5_qubit()),
            expected_state=ExpectedStatesGenericFiveQubit().get_logical_zero_state_vector(),
            initial_data_state=tensor(*[KET_ZERO_STATE_VECTOR] * 5),
        ),
        one=ParametersForStateEncodingTest(
            code=GenericStabilizerCode(generators=get_check_matrix_values_5_qubit()),
            expected_state=ExpectedStatesGenericFiveQubit().get_logical_one_state_vector(),
            initial_data_state=tensor(*[KET_ZERO_STATE_VECTOR] * 4, KET_ONE_STATE_VECTOR),
        ),
    ),
    "GenericStabilizerCodeStaeneCode": StateParameters(
        zero=ParametersForStateEncodingTest(
            code=GenericStabilizerCode(generators=get_check_matrix_values_steane()),
            expected_state=ExpectedStatesGenericSteane().get_logical_zero_state_vector(),
            initial_data_state=tensor(*[KET_ZERO_STATE_VECTOR] * 7),
        ),
        one=ParametersForStateEncodingTest(
            code=GenericStabilizerCode(generators=get_check_matrix_values_steane()),
            expected_state=ExpectedStatesGenericSteane().get_logical_one_state_vector(),
            initial_data_state=tensor(*[KET_ZERO_STATE_VECTOR] * 6, KET_ONE_STATE_VECTOR),
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
            initial_data_state=tensor(KET_ONE_DENSITY_MATRIX, *[KET_ZERO_DENSITY_MATRIX] * 8),
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

    def test_encoding(self):
        circuit = self._parameters.code.encode_logical_qubit()
        utilities = get_error_correcting_code_utilities(state=self._parameters.initial_data_state)
        data_state = utilities.get_state_after_circuit(circuit=circuit,
                                                       num_data_qubits=len(self._parameters.code.data_qubits),
                                                       initial_data_state=self._parameters.initial_data_state).state
        assert states_are_equal(data_state, self._parameters.expected_state)
