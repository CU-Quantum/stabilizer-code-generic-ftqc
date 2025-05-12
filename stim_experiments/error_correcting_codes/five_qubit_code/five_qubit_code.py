from dataclasses import dataclass, field
from functools import cached_property
from typing import Optional, Tuple
from uuid import uuid4

from cirq import Circuit, CircuitOperation, ClassicalDataStoreReader, Condition, FrozenCircuit, Gate, H, I, \
    KeyCondition, LineQubit, \
    MeasurementKey, \
    Operation, R, X, \
    Y, Z
from stim_experiments.error_correcting_codes.custom_dataclasses.recovery import RecoveryGates, RecoveryOperations
from stim_experiments.error_correcting_codes.error_correcting_code.error_correcting_code import ErrorCorrectingCode
from stim_experiments.custom_dataclasses.logical_operation import LogicalGateLabel, LogicalOperation
from stim_experiments.error_correcting_codes.support.fault_tolerant_error_correction.fault_tolerant_error_correction import \
    FaultTolerantErrorCorrection
from stim_experiments.error_correcting_codes.support.fault_tolerant_measurer.fault_tolerant_measurer import \
    OperationsApplierUsingCatState, FaultTolerantMeasurer
from stim_experiments.error_correcting_codes.support.fault_tolerant_state_encoder.fault_tolerant_state_encoder import \
    FaultTolerantStateEncoder
from stim_experiments.utilities import FreshAncillasPool


class FiveQubitCode(ErrorCorrectingCode):
    _generators = [
        [X, Z, Z, X, I],
        [I, X, Z, Z, X],
        [X, I, X, Z, Z],
        [Z, X, I, X, Z],
    ]

    @property
    def _flip_corrections(self):
        return [
            [self.data_qubits[i] for i in (0, 2)],
            [self.data_qubits[i] for i in (0,1,2,3)],
            [self.data_qubits[i] for i in (0,1,3,4)],
            [self.data_qubits[i] for i in (1,4)],
        ]

    def __init__(self, qubit_start_index: int = 0):
        super().__init__(num_data_qubits=5,
                         num_logical_qubits=1,
                         qubit_start_index=qubit_start_index)

    def encode_logical_qubit(self) -> Circuit:
        phase_corrections = [self._get_phase_corrections(generator_index=generator_index)
                             for generator_index in range(len(self._generators))]
        return FaultTolerantStateEncoder(generators=self._generator_operations, phase_corrections=phase_corrections).encode_state()

    def _get_phase_corrections(self, generator_index: int) -> list[Operation]:
        fix_qubits = self._flip_corrections[generator_index]
        return [Z(fix_qubit) for fix_qubit in fix_qubits]

    def _perform_get_operation_circuit(self, operation: LogicalOperation) -> None:
        pass

    @property
    def implemented_operations(self) -> list[LogicalGateLabel]:
        return []

    def get_error_correction_circuit(self) -> Circuit:
        recoveries = [
            RecoveryOperations(
                operation=Z(self.data_qubits[0]),
                symptom=[1, 0, 1, 0]
            ),
            RecoveryOperations(
                operation=Z(self.data_qubits[1]),
                symptom=[0, 1, 0, 1]
            ),
            RecoveryOperations(
                operation=Z(self.data_qubits[2]),
                symptom=[0, 0, 1, 0]
            ),
            RecoveryOperations(
                operation=Z(self.data_qubits[3]),
                symptom=[1, 0, 0, 1]
            ),
            RecoveryOperations(
                operation=Z(self.data_qubits[4]),
                symptom=[0, 1, 0, 0]
            ),
            RecoveryOperations(
                operation=X(self.data_qubits[0]),
                symptom=[0, 0, 0, 1]
            ),
            RecoveryOperations(
                operation=X(self.data_qubits[1]),
                symptom=[1, 0, 0, 0]
            ),
            RecoveryOperations(
                operation=X(self.data_qubits[2]),
                symptom=[1, 1, 0, 0]
            ),
            RecoveryOperations(
                operation=X(self.data_qubits[3]),
                symptom=[0, 1, 1, 0]
            ),
            RecoveryOperations(
                operation=X(self.data_qubits[4]),
                symptom=[0, 0, 1, 1]
            ),
            RecoveryOperations(
                operation=Y(self.data_qubits[0]),
                symptom=[1, 0, 1, 1]
            ),
            RecoveryOperations(
                operation=Y(self.data_qubits[1]),
                symptom=[1, 1, 0, 1]
            ),
            RecoveryOperations(
                operation=Y(self.data_qubits[2]),
                symptom=[1, 1, 1, 0]
            ),
            RecoveryOperations(
                operation=Y(self.data_qubits[3]),
                symptom=[1, 1, 1, 1]
            ),
            RecoveryOperations(
                operation=Y(self.data_qubits[4]),
                symptom=[0, 1, 1, 1]
            ),
        ]

        return FaultTolerantErrorCorrection(generator_operations=self._generator_operations,
                                            recoveries=recoveries).get_error_correction_circuit()

    @cached_property
    def _generator_operations(self) -> list[list[Operation]]:
        return [
            [gate(self.data_qubits[target_index]) for target_index, gate in enumerate(gates)]
            for gates in self._generators
        ]
