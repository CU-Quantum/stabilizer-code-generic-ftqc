from dataclasses import dataclass, field
from functools import cached_property
from typing import Optional, Tuple
from uuid import uuid4

from cirq import Circuit, CircuitOperation, ClassicalDataStoreReader, Condition, FrozenCircuit, Gate, H, I, \
    KeyCondition, LineQubit, \
    MeasurementKey, \
    Operation, R, X, \
    Y, Z
from stim_experiments.error_correcting_codes.custom_dataclasses.recovery import Recovery
from stim_experiments.error_correcting_codes.error_correcting_code.error_correcting_code import ErrorCorrectingCode
from stim_experiments.custom_dataclasses.logical_operation import LogicalGateLabel, LogicalOperation
from stim_experiments.error_correcting_codes.support.fault_tolerant_measurer.fault_tolerant_measurer import \
    OperationsApplierUsingCatState, FaultTolerantMeasurer
from stim_experiments.utilities import FreshAncillasPool


@dataclass(frozen=True)
class RecoveryCondition(Condition):
    # TODO test class
    key: MeasurementKey
    symptom: list[int] = field(default_factory=list)

    @property
    def keys(self) -> Tuple[MeasurementKey, ...]:
        return (self.key,)

    def replace_key(self, current: MeasurementKey, replacement: MeasurementKey):
        return RecoveryCondition(replacement, self.symptom) if self.key == current else self

    def resolve(self, classical_data: ClassicalDataStoreReader) -> bool:
        if self.key not in classical_data.keys():
            raise ValueError(f'Measurement key {self.key} missing when checking for recovery')
        measurements = [x[0] for x in classical_data.records[self.key]]
        return measurements == self.symptom

    @property
    def qasm(self):
        raise ValueError('QASM is defined only for SympyConditions of type key == constant.')


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
        measurement_keys = [MeasurementKey(f'FIVE_QUBIT_ENCODE_{i}_{uuid4()}') for i in range(len(self._generators))]
        return Circuit(
            [
                [
                    FaultTolerantMeasurer(operations=[gate(self.data_qubits[target_index])
                                                  for target_index, gate in enumerate(gates)],
                                      measurement_key=measurement_key).get_measurement_circuit(),
                    CircuitOperation(
                        FrozenCircuit(self._get_phase_corrections(generator_index=generator_index)),
                    ).with_classical_controls(measurement_key),
                ]
                for generator_index, (measurement_key, gates) in enumerate(zip(measurement_keys, self._generators))
            ],
        )

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
            Recovery(
                gate=Z,
                qubit_index=0,
                symptom=[1, 0, 1, 0]
            ),
            Recovery(
                gate=Z,
                qubit_index=1,
                symptom=[0, 1, 0, 1]
            ),
            Recovery(
                gate=Z,
                qubit_index=2,
                symptom=[0, 0, 1, 0]
            ),
            Recovery(
                gate=Z,
                qubit_index=3,
                symptom=[1, 0, 0, 1]
            ),
            Recovery(
                gate=Z,
                qubit_index=4,
                symptom=[0, 1, 0, 0]
            ),
            Recovery(
                gate=X,
                qubit_index=0,
                symptom=[0, 0, 0, 1]
            ),
            Recovery(
                gate=X,
                qubit_index=1,
                symptom=[1, 0, 0, 0]
            ),
            Recovery(
                gate=X,
                qubit_index=2,
                symptom=[1, 1, 0, 0]
            ),
            Recovery(
                gate=X,
                qubit_index=3,
                symptom=[0, 1, 1, 0]
            ),
            Recovery(
                gate=X,
                qubit_index=4,
                symptom=[0, 0, 1, 1]
            ),
            Recovery(
                gate=Y,
                qubit_index=0,
                symptom=[1, 0, 1, 1]
            ),
            Recovery(
                gate=Y,
                qubit_index=1,
                symptom=[1, 1, 0, 1]
            ),
            Recovery(
                gate=Y,
                qubit_index=2,
                symptom=[1, 1, 1, 0]
            ),
            Recovery(
                gate=Y,
                qubit_index=3,
                symptom=[1, 1, 1, 1]
            ),
            Recovery(
                gate=Y,
                qubit_index=4,
                symptom=[0, 1, 1, 1]
            ),
        ]

        measurement_key = MeasurementKey(f'FIVE_QUBIT_RECOVERY_{uuid4()}')

        recovery_circuit = Circuit(
            [
                recovery.gate(self.data_qubits[recovery.qubit_index])
                    .with_classical_controls(RecoveryCondition(key=measurement_key, symptom=recovery.symptom))
                for recovery in recoveries
            ],
        )

        return Circuit(
            self._get_syndrome_circuit(measurement_key=measurement_key),
            recovery_circuit,
        )

    def _get_syndrome_circuit(self, measurement_key: Optional[MeasurementKey] = None) -> Circuit:
        return Circuit(
            FaultTolerantMeasurer(operations=[gate(self.data_qubits[target_index]) for target_index, gate in enumerate(gates)],
                                  measurement_key=measurement_key,
                                  ).get_measurement_circuit()
            for gates in self._generators
        )

    @cached_property
    def _generators_with_measurement_keys(self) -> dict[MeasurementKey, list[Gate]]:
        return {MeasurementKey(f'FIVE_QUBIT_CODE_{i}_{uuid4()}'): generator
                for i, generator in enumerate(self._generators)}
