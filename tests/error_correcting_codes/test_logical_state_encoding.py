from dataclasses import dataclass

import pytest
from cirq import LineQubit

from stim_experiments.error_correcting_codes.error_correcting_code.error_correcting_code import ErrorCorrectingCode
from stim_experiments.error_correcting_codes.error_correcting_code_utilities import \
    get_error_correcting_code_utilities
from stim_experiments.error_correcting_codes.five_qubit_code.five_qubit_code import FiveQubitCode
from stim_experiments.error_correcting_codes.generic_stabilizer_code.generic_stabilizer_code import \
    GenericStabilizerCode
from stim_experiments.error_correcting_codes.shors_code.shors_repetition_code import ShorsRepetitionCode
from stim_experiments.error_correcting_codes.steane_code.staene_code import SteaneCode
from stim_experiments.error_correcting_codes.three_cat_code.three_cat_code import ThreeCatCode
from stim_experiments.utilities import FreshAncillasPool, KET_ONE_DENSITY_MATRIX, KET_ONE_STATE_VECTOR, \
    KET_ZERO_DENSITY_MATRIX, \
    KET_ZERO_STATE_VECTOR, TYPE_STATE_VECTOR_OR_DENSITY_MATRIX, tensor, trace_out_ancillas_in_zero_state
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
    # "ThreeCatCode": StateParameters(
    #     zero=ParametersForStateEncodingTest(
    #         code=ThreeCatCode(num_qubits_in_cat_state=ExpectedStatesThreeCat().arbitrary_num_qubits),
    #         expected_state=ExpectedStatesThreeCat().get_logical_zero_state_vector(),
    #         initial_data_state=tensor(*[KET_ZERO_STATE_VECTOR] * ExpectedStatesThreeCat().arbitrary_num_qubits * ThreeCatCode.num_repetitions),
    #     ),
    #     one=ParametersForStateEncodingTest(
    #         code=ThreeCatCode(num_qubits_in_cat_state=ExpectedStatesThreeCat().arbitrary_num_qubits),
    #         expected_state=ExpectedStatesThreeCat().get_logical_one_state_vector(),
    #         initial_data_state=tensor(*[tensor(KET_ONE_STATE_VECTOR, *[KET_ZERO_STATE_VECTOR] * (ExpectedStatesThreeCat().arbitrary_num_qubits - 1))] * ThreeCatCode.num_repetitions),
    #     ),
    # ),
    "GenericStabilizerCodeFiveQubit": StateParameters(
        zero=ParametersForStateEncodingTest(
            code=GenericStabilizerCode(generators=get_check_matrix_values_5_qubit()),
            expected_state=ExpectedStatesGenericFiveQubit().get_logical_zero_density_matrix(),
            initial_data_state=tensor(*[KET_ZERO_STATE_VECTOR] * 5),
        ),
        one=ParametersForStateEncodingTest(
            code=GenericStabilizerCode(generators=get_check_matrix_values_5_qubit()),
            expected_state=ExpectedStatesGenericFiveQubit().get_logical_one_density_matrix(),
            initial_data_state=tensor(*[KET_ONE_STATE_VECTOR] * 5),
        ),
    ),
    # "GenericStabilizerCodeStaeneQubit": StateParameters(
    #     zero=ParametersForStateEncodingTest(
    #         code=GenericStabilizerCode(generators=get_check_matrix_values_steane(), initial_logical_qubit_state=KET_ZERO_DENSITY_MATRIX),
    #         expected_state=ExpectedStatesGenericSteane().get_logical_zero_density_matrix(),
    #         initial_data_state=KET_ZERO_STATE_VECTOR,
    #     ),
    #     one=ParametersForStateEncodingTest(
    #         code=GenericStabilizerCode(generators=get_check_matrix_values_steane(), initial_logical_qubit_state=KET_ZERO_DENSITY_MATRIX),
    #         expected_state=ExpectedStatesGenericSteane().get_logical_one_density_matrix(),
    #         initial_data_state=KET_ONE_STATE_VECTOR,
    #     ),
    # ),
    "FiveQubitCode": StateParameters(
        zero=ParametersForStateEncodingTest(
            code=FiveQubitCode(),
            expected_state=ExpectedStatesFiveQubit().get_logical_zero_density_matrix(),
            initial_data_state=tensor(*[KET_ZERO_STATE_VECTOR] * 5),
        ),
        one=ParametersForStateEncodingTest(
            code=FiveQubitCode(),
            expected_state=ExpectedStatesThreeCat().get_logical_one_state_vector(),
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


PARAMETERS_FLATTENED = [parameters for states in PARAMETERS.values() for parameters in (states.zero, states.one)]


class TestLogicalStateEncoding:
    @pytest.fixture(autouse=True)
    def _setup(self):
        FreshAncillasPool().reset()

    @pytest.mark.parametrize('parameters', PARAMETERS_FLATTENED)
    def test_encoding(self, parameters: ParametersForStateEncodingTest):
        FreshAncillasPool().set_first_ancilla_num(first_ancilla_num=len(parameters.code.data_qubits))
        circuit = parameters.code.encode_logical_qubit()
        utilities = get_error_correcting_code_utilities(state=parameters.initial_data_state)
        qubits = LineQubit.range(utilities.get_max_qubit_index(circuit=circuit) + 1)
        num_ancillas = len(qubits) - len(parameters.code.data_qubits)
        initial_state = tensor(parameters.initial_data_state, *[utilities.zero_state] * num_ancillas)
        simulated_state = utilities.get_state_after_circuit(circuit=circuit,
                                                            qubit_order=qubits,
                                                            initial_state=initial_state).state
        data_state = trace_out_ancillas_in_zero_state(state=simulated_state, num_ancillas=num_ancillas)
        assert states_are_equal(data_state, parameters.expected_state)
