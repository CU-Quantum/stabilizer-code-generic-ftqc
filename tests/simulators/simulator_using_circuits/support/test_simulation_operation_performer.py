from typing import List

import numpy.random
import pytest
from cirq import Circuit, X, Z, kron
from numpy import array

from stim_experiments.custom_dataclasses.logical_operation import LogicalGateLabel, LogicalOperation
from stim_experiments.error_correcting_codes.error_correcting_code.error_correcting_code import ErrorCorrectingCode
from stim_experiments.error_correcting_codes.generic_stabilizer_code.custom_dataclasses.state_and_measurements import \
    StateAndMeasurements
from stim_experiments.simulators.simulator_using_circuits.custom_dataclasses.simulation_operation import \
    ControlEncoding, SimulationOperation, TargetEncoding
from stim_experiments.simulators.simulator_using_circuits.support.simulation_operation_performer import \
    SimulationOperationPerformer
from stim_experiments.utilities import KET_ONE_STATE_VECTOR, KET_ZERO_STATE_VECTOR, TYPE_STATE_VECTOR_OR_DENSITY_MATRIX


class ErrorCorrectingCodeStub(ErrorCorrectingCode):
    def __init__(self, qubit_start_index: int = 0):
        super().__init__(num_data_qubits=1,
                         num_ancilla_qubits=0,
                         num_logical_qubits=1,
                         initial_logical_qubit_state=KET_ZERO_STATE_VECTOR,
                         qubit_start_index=qubit_start_index)

    def encode_logical_qubit(self) -> TYPE_STATE_VECTOR_OR_DENSITY_MATRIX:
        return self._initial_logical_qubit_state

    def get_error_correction_circuit(self) -> Circuit:
        pass

    def _perform_get_operation_circuit(self, operation: LogicalOperation) -> Circuit:
        if operation.gate == LogicalGateLabel.X:
            return Circuit(X(self.data_qubits[0]))
        else:
            return Circuit(Z(self.data_qubits[0]))

    @property
    def _implemented_operations(self) -> List[LogicalGateLabel]:
        return [LogicalGateLabel.X, LogicalGateLabel.Z]


class TestSimulationOperationPerformer:
    def test_blank_simulation_operation(self):
        code = ErrorCorrectingCodeStub()
        operation = SimulationOperation()
        with pytest.raises(ValueError, match="Was given a SimulationOperation with no encoding."):
            performer = SimulationOperationPerformer(operation=operation,
                                                     current_state=StateAndMeasurements(
                                                         state=KET_ZERO_STATE_VECTOR,
                                                         measurements=array([]),
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
                                                     measurements=array([]),
                                                 ),
                                                 qubits=code.all_qubits)
        result = performer.perform_operation()
        assert result == StateAndMeasurements(
            state=KET_ONE_STATE_VECTOR,
            measurements=array([])
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
                                                     measurements=array([]),
                                                 ),
                                                 qubits=qubits)
        result = performer.perform_operation()
        expected_state = kron(KET_ONE_STATE_VECTOR, KET_ONE_STATE_VECTOR, shape_len=1)
        assert result == StateAndMeasurements(
            state=expected_state,
            measurements=array([])
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
                                                     measurements=array([]),
                                                 ),
                                                 qubits=qubits)
        result = performer.perform_operation()
        assert result == StateAndMeasurements(
            state=initial_state,
            measurements=array([])
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
                                                         measurements=array([]),
                                                     ),
                                                     qubits=qubits)
            result = performer.perform_operation()
            assert result == StateAndMeasurements(
                state=initial_state,
                measurements=array([0])
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
                                                         measurements=array([]),
                                                     ),
                                                     qubits=qubits)
            result = performer.perform_operation()
            assert result == StateAndMeasurements(
                state=initial_state,
                measurements=array([1])
            )

    def test_multiqubit_measurement(self):
        assert False
