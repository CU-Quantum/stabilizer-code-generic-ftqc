import pytest
from cirq import LineQubit

from stim_experiments.algorithms.support.logical_operations_circuit_creator.support.circuit_from_operation_creator import \
    CircuitFromOperationCreator
from stim_experiments.custom_dataclasses.logical_operation import LogicalGateLabel, LogicalOperation
from stim_experiments.custom_dataclasses.simulation_operation import SimulationOperation, TargetEncoding, LogicalEncodingIndex
from stim_experiments.globals.fresh_ancillas_pool import FreshAncillasPool
from stim_experiments.simulations.error_correcting_simulator import get_error_correcting_simulator
from stim_experiments.utilities.utilities import KET_ONE_STATE_VECTOR, KET_ZERO_STATE_VECTOR, \
    states_are_equal, tensor
from tests.algorithms.support.logical_operations_circuit_creator.support.circuit_from_operation_creator.error_correcting_code_stub_with_x_and_z import \
    ErrorCorrectingCodeStubWithXAndZ
from tests.utilities_for_tests import set_configuration_to_reduce_ancilla_qubits


class TestCircuitFromOperationCreator:
    @pytest.fixture(autouse=True)
    def _setup(self):
        set_configuration_to_reduce_ancilla_qubits()

    def test_create_circuit_with_controlled_operation(self):
        qubits = LineQubit.range(2)
        FreshAncillasPool().set_first_ancilla_num(first_ancilla_num=len(qubits))

        target_encoding = TargetEncoding(
            operation=LogicalOperation(
                gate=LogicalGateLabel.X,
                qubit_index=0,
            ),
            encoding=ErrorCorrectingCodeStubWithXAndZ(qubits=qubits[1:]),
        )
        control_encoding = LogicalEncodingIndex(
            encoding=ErrorCorrectingCodeStubWithXAndZ(qubits=qubits[:1]),
            qubit_index_relative=0,
            qubit_index_logical=0,
        )
        operation = SimulationOperation(
            target_encoding=target_encoding,
            control_encoding=control_encoding,
        )

        utilities = get_error_correcting_simulator(state=KET_ZERO_STATE_VECTOR)
        circuit = CircuitFromOperationCreator(operation=operation).create_circuit()
        simulated_state_with_inactive_control = utilities.get_state_after_circuit(
            circuit=circuit,
            num_data_qubits=len(qubits),
        ).state
        simulated_state_with_active_control = utilities.get_state_after_circuit(
            circuit=circuit,
            num_data_qubits=len(qubits),
            initial_data_state=tensor(KET_ONE_STATE_VECTOR, KET_ZERO_STATE_VECTOR),
        ).state
        assert states_are_equal(simulated_state_with_inactive_control, tensor(KET_ZERO_STATE_VECTOR, KET_ZERO_STATE_VECTOR))
        assert states_are_equal(simulated_state_with_active_control, tensor(KET_ONE_STATE_VECTOR, KET_ONE_STATE_VECTOR))

    def test_create_circuit_with_control_encoding_only_indicates_measurement(self):
        arbitrary_logical_qubit_num = 10
        control_encoding = LogicalEncodingIndex(
            encoding=ErrorCorrectingCodeStubWithXAndZ(),
            qubit_index_relative=0,
            qubit_index_logical=arbitrary_logical_qubit_num,
        )
        operation = SimulationOperation(
            control_encoding=control_encoding,
        )
        FreshAncillasPool().set_first_ancilla_num(first_ancilla_num=len(control_encoding.encoding.data_qubits))

        utilities = get_error_correcting_simulator(state=KET_ZERO_STATE_VECTOR)
        circuit = CircuitFromOperationCreator(operation=operation).create_circuit()
        simulation = utilities.get_state_after_circuit(
            circuit=circuit,
            num_data_qubits=len(control_encoding.encoding.data_qubits),
        )
        assert simulation.measurements[str(arbitrary_logical_qubit_num)][0] == 0

    def test_create_circuit_with_no_encoding_raises_error(self):
        operation = SimulationOperation()
        creator = CircuitFromOperationCreator(operation=operation)
        with pytest.raises(ValueError, match='^Was given a SimulationOperation with no encoding\\.$'):
            creator.create_circuit()
