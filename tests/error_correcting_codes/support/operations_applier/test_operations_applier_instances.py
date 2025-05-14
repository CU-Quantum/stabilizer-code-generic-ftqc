from typing import Optional

import pytest
import sympy
from cirq import Circuit, H, LineQubit, Operation, X

from stim_experiments.error_correcting_codes.error_correcting_code_utilities import get_error_correcting_code_utilities
from stim_experiments.error_correcting_codes.support.operations_applier.operations_applier_using_cat_state.operations_applier_using_cat_state import \
    OperationsApplierUsingCatStateControl
from stim_experiments.error_correcting_codes.support.operations_applier.operations_applier_using_single_qubit_hadamard_control import \
    OperationsApplierUsingSingleQubitHadamardControl
from stim_experiments.utilities import KET_ONE_STATE_VECTOR, KET_ZERO_STATE_VECTOR, TYPE_STATE_VECTOR, tensor
from tests.utilities import states_are_equal


class TestOperationsApplierInstances:
    @pytest.fixture(autouse=True, params=[
        pytest.param(OperationsApplierUsingSingleQubitHadamardControl, id='OperationsApplierUsingSingleQubitControl'),
        pytest.param(OperationsApplierUsingCatStateControl, id='OperationsApplierUsingCatStateControl'),
    ])
    def _set_operation_applier_instance(self, request):
        self._operation_applier_type = request.param

    def test_trivial(self):
        applier = OperationsApplierUsingSingleQubitHadamardControl(operations=[], measurement_qubit=LineQubit(0))
        circuit = applier.get_application_circuit()
        assert circuit == Circuit()

    def test_one_operation(self):
        data_qubits = LineQubit.range(1)

        operations = [X(data_qubits[0])]
        expected_state = tensor(*[KET_ONE_STATE_VECTOR] * len(data_qubits))
        assert self._operations_result_in_expected_state(operations=operations,
                                                         expected_state=expected_state)

    def test_two_operations(self):
        data_qubits = LineQubit.range(2)

        operations = [X(qubit) for qubit in data_qubits]
        expected_state = tensor(*[KET_ONE_STATE_VECTOR] * len(data_qubits))
        assert self._operations_result_in_expected_state(operations=operations,
                                                         expected_state=expected_state)

    def test_condition(self):
        data_qubits = LineQubit.range(1)

        operations = [X(data_qubits[0])]
        expected_state = tensor(*[KET_ZERO_STATE_VECTOR] * len(data_qubits))
        self._operations_result_in_expected_state(operations=operations,
                                                  expected_state=expected_state,
                                                  condition=sympy.false)

    def _operations_result_in_expected_state(self,
                                             operations: list[Operation],
                                             expected_state: TYPE_STATE_VECTOR,
                                             condition: Optional[sympy.Expr] = None) -> bool:
        num_data_qubits = len(operations)
        measurement_qubit = LineQubit(num_data_qubits)
        applier = self._operation_applier_type(operations=operations,
                                               measurement_qubit=measurement_qubit,
                                               condition=condition)
        circuit = Circuit(
            X(measurement_qubit),
            H(measurement_qubit),
            applier.get_application_circuit(),
            X(measurement_qubit),
        )
        utilities = get_error_correcting_code_utilities(state=KET_ZERO_STATE_VECTOR)
        simulation = utilities.get_state_after_circuit(circuit=circuit,
                                                       num_data_qubits=num_data_qubits)
        return states_are_equal(simulation.state, expected_state)
