from functools import cached_property
from typing import Optional

from cirq import Circuit, I, LineQubit, Operation, X, Y, Z
from stim_experiments.custom_dataclasses.recovery import RecoveryGates
from stim_experiments.error_correcting_codes.error_correcting_code.error_correcting_code import ErrorCorrectingCode
from stim_experiments.custom_dataclasses.logical_operation import LogicalOperation
from stim_experiments.error_correcting_codes.support.error_recovery.error_recovery_by_generator_measurement import \
    ErrorRecoveryByGeneratorMeasurement
from stim_experiments.error_correcting_codes.support.state_encoder.state_encoder_by_generator_measurement import \
    StateEncoderByGeneratorMeasurement


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

    def __init__(self, qubits: Optional[list[LineQubit]] = None):
        super().__init__(num_data_qubits=5,
                         num_logical_qubits=1,
                         qubits=qubits)
    def encode_logical_qubit(self) -> Circuit:
        phase_corrections = [self._get_phase_corrections(generator_index=generator_index)
                             for generator_index in range(len(self._generators))]
        return StateEncoderByGeneratorMeasurement(generators=self._generator_operations, phase_corrections=phase_corrections).encode_state()

    def _get_phase_corrections(self, generator_index: int) -> list[Operation]:
        fix_qubits = self._flip_corrections[generator_index]
        return [Z(fix_qubit) for fix_qubit in fix_qubits]

    def _perform_get_operation_circuit(self, operation: LogicalOperation) -> None:
        pass

    def get_error_correction_circuit(self) -> Circuit:
        recoveries = [
            RecoveryGates(
                gate=Z,
                qubit_index=0,
                symptom=[1, 0, 1, 0]
            ),
            RecoveryGates(
                gate=Z,
                qubit_index=1,
                symptom=[0, 1, 0, 1]
            ),
            RecoveryGates(
                gate=Z,
                qubit_index=2,
                symptom=[0, 0, 1, 0]
            ),
            RecoveryGates(
                gate=Z,
                qubit_index=3,
                symptom=[1, 0, 0, 1]
            ),
            RecoveryGates(
                gate=Z,
                qubit_index=4,
                symptom=[0, 1, 0, 0]
            ),
            RecoveryGates(
                gate=X,
                qubit_index=0,
                symptom=[0, 0, 0, 1]
            ),
            RecoveryGates(
                gate=X,
                qubit_index=1,
                symptom=[1, 0, 0, 0]
            ),
            RecoveryGates(
                gate=X,
                qubit_index=2,
                symptom=[1, 1, 0, 0]
            ),
            RecoveryGates(
                gate=X,
                qubit_index=3,
                symptom=[0, 1, 1, 0]
            ),
            RecoveryGates(
                gate=X,
                qubit_index=4,
                symptom=[0, 0, 1, 1]
            ),
            RecoveryGates(
                gate=Y,
                qubit_index=0,
                symptom=[1, 0, 1, 1]
            ),
            RecoveryGates(
                gate=Y,
                qubit_index=1,
                symptom=[1, 1, 0, 1]
            ),
            RecoveryGates(
                gate=Y,
                qubit_index=2,
                symptom=[1, 1, 1, 0]
            ),
            RecoveryGates(
                gate=Y,
                qubit_index=3,
                symptom=[1, 1, 1, 1]
            ),
            RecoveryGates(
                gate=Y,
                qubit_index=4,
                symptom=[0, 1, 1, 1]
            ),
        ]

        return ErrorRecoveryByGeneratorMeasurement(generator_operations=self._generator_operations,
                                                   qubits=self.data_qubits,
                                                   recoveries=recoveries).get_error_correction_circuit()

    @cached_property
    def _generator_operations(self) -> list[list[Operation]]:
        return [
            [gate(self.data_qubits[target_index]) for target_index, gate in enumerate(gates)]
            for gates in self._generators
        ]
