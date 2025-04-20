import numpy.random
import pytest
from cirq import kron

from stim_experiments.custom_dataclasses.logical_operation import LogicalGateLabel, LogicalOperation
from stim_experiments.error_correcting_codes.generic_stabilizer_code.custom_dataclasses.state_and_measurements import \
    StateAndMeasurements
from stim_experiments.simulators.simulator_using_circuits.custom_dataclasses.simulation_operation import \
    ControlEncoding, SimulationOperation, TargetEncoding
from stim_experiments.simulators.simulator_using_circuits.support.simulation_operation_performer import \
    SimulationOperationPerformer
from stim_experiments.utilities import KET_ONE_STATE_VECTOR, KET_ZERO_STATE_VECTOR
from tests.simulators.simulator_using_circuits.support.simulation_operation_performer.error_correcting_code_stub import \
    ErrorCorrectingCodeStub


class TestSimulationOperationPerformer:
    def test_blank_simulation_operation(self):
        code = ErrorCorrectingCodeStub()
        operation = SimulationOperation()
        with pytest.raises(ValueError, match="Was given a SimulationOperation with no encoding."):
            performer = SimulationOperationPerformer(operation=operation,
                                                     current_state=StateAndMeasurements(
                                                         state=KET_ZERO_STATE_VECTOR,
                                                     ),
                                                     qubits=code.all_qubits)
            performer.perform_operation()

    def test_target_operation_only(self):
        code = ErrorCorrectingCodeStub()
        operation = SimulationOperation(
            target_encoding=TargetEncoding(
                operation=LogicalOperation(
                    LogicalGateLabel.X,
                    qubit_index=0
                ),
                encoding=code,
            )
        )
        performer = SimulationOperationPerformer(operation=operation,
                                                 current_state=StateAndMeasurements(
                                                     state=KET_ZERO_STATE_VECTOR,
                                                 ),
                                                 qubits=code.all_qubits)
        result = performer.perform_operation()
        assert result == StateAndMeasurements(
            state=KET_ONE_STATE_VECTOR,
            measurements={},
        )

    def test_target_operation_with_control_activated(self):
        target_code = ErrorCorrectingCodeStub()
        control_code = ErrorCorrectingCodeStub(qubit_start_index=1)
        operation = SimulationOperation(
            target_encoding=TargetEncoding(
                operation=LogicalOperation(
                    LogicalGateLabel.X,
                    qubit_index=0
                ),
                encoding=target_code,
            ),
            control_encoding=ControlEncoding(
                encoding=control_code,
                qubit_index=0
            )
        )
        initial_state = kron(KET_ZERO_STATE_VECTOR, KET_ONE_STATE_VECTOR, shape_len=1)
        qubits = target_code.all_qubits + control_code.all_qubits
        performer = SimulationOperationPerformer(operation=operation,
                                                 current_state=StateAndMeasurements(
                                                     state=initial_state,
                                                 ),
                                                 qubits=qubits)
        result = performer.perform_operation()
        expected_state = kron(KET_ONE_STATE_VECTOR, KET_ONE_STATE_VECTOR, shape_len=1)
        assert result == StateAndMeasurements(
            state=expected_state,
            measurements={},
        )

    def test_target_operation_with_control_unactivated(self):
        target_code = ErrorCorrectingCodeStub()
        control_code = ErrorCorrectingCodeStub(qubit_start_index=1)
        operation = SimulationOperation(
            target_encoding=TargetEncoding(
                operation=LogicalOperation(
                    LogicalGateLabel.X,
                    qubit_index=0
                ),
                encoding=target_code,
            ),
            control_encoding=ControlEncoding(
                encoding=control_code,
                qubit_index=0
            )
        )
        initial_state = kron(KET_ZERO_STATE_VECTOR, KET_ZERO_STATE_VECTOR, shape_len=1)
        qubits = target_code.all_qubits + control_code.all_qubits
        performer = SimulationOperationPerformer(operation=operation,
                                                 current_state=StateAndMeasurements(
                                                     state=initial_state,
                                                 ),
                                                 qubits=qubits)
        result = performer.perform_operation()
        assert result == StateAndMeasurements(
            state=initial_state,
            measurements={},
        )

    def test_measurement_operation_zero(self):
        numpy.random.seed(0)
        num_trials = 5
        for _ in range(num_trials):
            control_code = ErrorCorrectingCodeStub()
            operation = SimulationOperation(
                control_encoding=ControlEncoding(
                    encoding=control_code,
                    qubit_index=0
                )
            )
            initial_state = KET_ZERO_STATE_VECTOR
            qubits = control_code.all_qubits
            performer = SimulationOperationPerformer(operation=operation,
                                                     current_state=StateAndMeasurements(
                                                         state=initial_state,
                                                     ),
                                                     qubits=qubits)
            result = performer.perform_operation()
            assert result == StateAndMeasurements(
                state=initial_state,
                measurements={0: [0]}
            )

    def test_measurement_operation_one(self):
        numpy.random.seed(0)
        num_trials = 5
        for _ in range(num_trials):
            control_code = ErrorCorrectingCodeStub()
            operation = SimulationOperation(
                control_encoding=ControlEncoding(
                    encoding=control_code,
                    qubit_index=0
                )
            )
            initial_state = KET_ONE_STATE_VECTOR
            qubits = control_code.all_qubits
            performer = SimulationOperationPerformer(operation=operation,
                                                     current_state=StateAndMeasurements(
                                                         state=initial_state,
                                                     ),
                                                     qubits=qubits)
            result = performer.perform_operation()
            assert result == StateAndMeasurements(
                state=initial_state,
                measurements={0: [1]}
            )
