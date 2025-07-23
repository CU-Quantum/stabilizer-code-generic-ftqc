from dataclasses import dataclass

import pytest
from cirq import Circuit, I
from numpy import sqrt

from stim_experiments.error_correcting_codes.error_correcting_code.error_correcting_code import ErrorCorrectingCode
from stim_experiments.custom_dataclasses.logical_operation import LogicalGateLabel, LogicalOperation
from stim_experiments.error_correcting_codes.five_qubit_code.five_qubit_code import FiveQubitCode
from stim_experiments.error_correcting_codes.repetition_code.repetition_code import RepetitionCodeOneLogical
from stim_experiments.error_correcting_codes.stabilizer_standardized_code.stabilizer_standardized_code import \
    StabilizerStandardizedCode
from stim_experiments.error_correcting_codes.shors_code.shors_repetition_code import ShorsRepetitionCode
from stim_experiments.error_correcting_codes.steane_code.staene_code import SteaneCode
from stim_experiments.error_correcting_codes.cat_parity_code.cat_parity_code import \
    CatParityCode
from stim_experiments.error_correcting_codes.support.multiple_cat_code.multiple_cat_code import MultipleCatCode
from stim_experiments.globals.fresh_ancillas_pool import FreshAncillasPool
from stim_experiments.simulations.error_correcting_simulator import get_error_correcting_simulator
from tests.error_correcting_codes.expected_states.expected_states import ExpectedStates
from tests.error_correcting_codes.five_qubit_code.expected_states_five_qubit import ExpectedStatesFiveQubit
from tests.error_correcting_codes.multiple_cat_code.expected_states_multiple_cat import ExpectedStatesMultipleCat
from tests.error_correcting_codes.stabilizer_standardized_code.expected_states_standardized_5_qubit import \
    ExpectedStatesGenericFiveQubit
from stim_experiments.utilities.predefined_check_matrix_values import get_check_matrix_values_5_qubit
from tests.error_correcting_codes.repetition_code.expected_states_repetition import ExpectedStatesRepetition
from tests.error_correcting_codes.shors_code.expected_states_shor import ExpectedStatesShor
from tests.error_correcting_codes.steane_code.expected_states_steane import ExpectedStatesSteane
from tests.error_correcting_codes.cat_parity_code.expected_states_cat_parity import \
    ExpectedStatesCatParity
from tests.utilities_for_tests import set_configuration_to_reduce_ancilla_qubits
from stim_experiments.utilities.utilities import states_are_equal


@dataclass
class ParametersForLogicalGatesTest:
    code: ErrorCorrectingCode
    expected_states: ExpectedStates


PARAMETERS = {
    "MultipleCatCode":ParametersForLogicalGatesTest(
        code=MultipleCatCode(num_cats=ExpectedStatesMultipleCat().arbitrary_num_cats,
                             num_qubits_per_cat=ExpectedStatesMultipleCat().arbitrary_num_qubits_per_cat),
        expected_states=ExpectedStatesMultipleCat(),
    ),
    "RepetitionCode": ParametersForLogicalGatesTest(
        code=RepetitionCodeOneLogical(num_qubits=ExpectedStatesRepetition().arbitrary_num_qubits),
        expected_states=ExpectedStatesRepetition(),
    ),
    "CatParityCode": ParametersForLogicalGatesTest(
        code=CatParityCode(num_cats=ExpectedStatesCatParity().num_cats,
                           num_qubits_per_cat=ExpectedStatesCatParity().num_qubits_per_cat),
        expected_states=ExpectedStatesCatParity(),
    ),
    "GenericStabilizerCodeFiveQubit": ParametersForLogicalGatesTest(
        code=StabilizerStandardizedCode(generators=get_check_matrix_values_5_qubit()),
        expected_states=ExpectedStatesGenericFiveQubit()
    ),
    "FiveQubitCode": ParametersForLogicalGatesTest(
        code=FiveQubitCode(),
        expected_states=ExpectedStatesFiveQubit(),
    ),
    "SteaneCode": ParametersForLogicalGatesTest(
        code=SteaneCode(),
        expected_states=ExpectedStatesSteane(),
    ),
    "ShorsRepetitionCode": ParametersForLogicalGatesTest(
        code=ShorsRepetitionCode(),
        expected_states=ExpectedStatesShor(),
    ),
}


PARAMETERS_FLATTENED = [pytest.param(parameters, id=name) for name, parameters in PARAMETERS.items()]


class TestLogicalGates:
    @pytest.fixture(autouse=True, params=PARAMETERS_FLATTENED)
    def _setup(self, request):
        self._parameters: ParametersForLogicalGatesTest = request.param
        self._num_data_qubits = len(self._parameters.code.data_qubits)
        FreshAncillasPool().set_first_ancilla_num(first_ancilla_num=len(self._parameters.code.data_qubits))
        set_configuration_to_reduce_ancilla_qubits()

    def test_logical_x(self):
        target_index = self._parameters.code.num_logical_qubits - 1
        operation = LogicalOperation(gate=LogicalGateLabel.X, qubit_index=target_index)

        initial_data_state = self._parameters.expected_states.get_logical_zero_state_vector()
        expected_state = self._parameters.expected_states.get_logical_one_state_vector()

        utilities = get_error_correcting_simulator(state=initial_data_state)
        current_state = utilities.get_state_after_circuit(
            circuit=Circuit(
                [I(qubit) for qubit in self._parameters.code.data_qubits],
                self._parameters.code.get_operation_circuit(operation=operation)
            ),
            num_data_qubits=self._num_data_qubits,
            initial_data_state=initial_data_state,
        ).state
        assert states_are_equal(current_state, expected_state)

    def test_logical_z(self):
        target_index = self._parameters.code.num_logical_qubits - 1
        operation = LogicalOperation(gate=LogicalGateLabel.Z, qubit_index=target_index)

        initial_data_state = (1 / sqrt(2)) * (
            self._parameters.expected_states.get_logical_zero_state_vector()
            + self._parameters.expected_states.get_logical_one_state_vector()
        )
        expected_state = (1 / sqrt(2)) * (
            self._parameters.expected_states.get_logical_zero_state_vector()
            - self._parameters.expected_states.get_logical_one_state_vector()
        )

        utilities = get_error_correcting_simulator(state=initial_data_state)
        simulated_state = utilities.get_state_after_circuit(
            circuit=Circuit(
                [I(qubit) for qubit in self._parameters.code.data_qubits],
                self._parameters.code.get_operation_circuit(operation=operation)
            ),
            num_data_qubits=self._num_data_qubits,
            initial_data_state=initial_data_state,
        ).state
        assert states_are_equal(simulated_state, expected_state)
