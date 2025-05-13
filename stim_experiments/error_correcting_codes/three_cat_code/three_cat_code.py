from dataclasses import dataclass
from typing import Optional
from uuid import uuid4

from cirq import Circuit, CircuitOperation, ClassicalDataStoreReader, Condition, FrozenCircuit, LineQubit, \
    MeasurementKey, X, Z
from cirq.protocols import json_serialization

from stim_experiments.custom_dataclasses.logical_operation import LogicalGateLabel, LogicalOperation
from stim_experiments.error_correcting_codes.error_correcting_code.error_correcting_code import ErrorCorrectingCode
from stim_experiments.error_correcting_codes.support.cat_state_creator.cat_state_creator_flag_pattern import \
    CatStateCreatorFlagPattern
from stim_experiments.error_correcting_codes.support.fault_tolerant_measurer.fault_tolerant_measurer import \
    FaultTolerantMeasurer
from stim_experiments.error_correcting_codes.support.fault_tolerant_measurer.support.parity_verifier import \
    ParityVerifier
from stim_experiments.utilities import FreshAncillasPool


@dataclass(frozen=True)
class ParityCheckReader(Condition):
    # TODO test class
    key: MeasurementKey
    qubit_correction_index: int = 0

    @property
    def keys(self):
        return (self.key,)

    def replace_key(self, current: MeasurementKey, replacement: MeasurementKey):
        return ParityCheckReader(replacement, self.qubit_correction_index) if self.key == current else self

    def __str__(self):
        return str(self.key)

    def __repr__(self):
        return f'ParityCheckIndexLimit({self.key!r}, f{self.qubit_correction_index})'

    def resolve(self, classical_data: ClassicalDataStoreReader) -> bool:
        if self.key not in classical_data.keys():
            raise ValueError(f'Measurement key {self.key} missing when testing classical control')
        measurements = [x[0] for x in classical_data.records[self.key]]
        if not self.qubit_correction_index:
            return measurements[self.qubit_correction_index] and not measurements[self.qubit_correction_index + 1]
        elif self.qubit_correction_index == len(measurements):
            return not measurements[self.qubit_correction_index - 2] and measurements[self.qubit_correction_index - 1]
        else:
            return bool(measurements[self.qubit_correction_index - 1] and measurements[self.qubit_correction_index])

    def _json_dict_(self):
        return json_serialization.dataclass_json_dict(self)

    @classmethod
    def _from_json_dict_(cls, key, qubit_correction_index, **kwargs):
        return cls(key=key, qubit_correction_index=qubit_correction_index)

    @property
    def qasm(self):
        raise ValueError('QASM is defined only for SympyConditions of type key == constant.')


class ThreeCatCode(ErrorCorrectingCode):
    num_cats = 3

    def __init__(self, num_qubits_in_cat_state: int, qubits: Optional[list[LineQubit]] = None):
        self._num_qubits_in_cat_state = num_qubits_in_cat_state
        super().__init__(num_data_qubits=num_qubits_in_cat_state * self.num_cats,
                         num_logical_qubits=1,
                         qubits=qubits)

    def encode_logical_qubit(self) -> Circuit:
        return Circuit(
            CatStateCreatorFlagPattern(qubit_register=self.data_qubits[i * self._num_qubits_in_cat_state:(i + 1) * self._num_qubits_in_cat_state]
                                       ).get_cat_state_circuit()
            for i in range(self.num_cats)
        )

    def get_error_correction_circuit(self) -> Circuit:
        return Circuit(
            self._correct_x_errors(),
            self._correct_z_errors()
        )

    def _correct_x_errors(self) -> Circuit:
        circuit = Circuit()
        for cat_index in range(self.num_cats):
            measurement_key = MeasurementKey(f"THREE_CAT_Z_STABILIZER_{cat_index}_{uuid4()}")
            circuit.append([
                [
                    FaultTolerantMeasurer(operations=[Z(self.data_qubits[cat_index * self._num_qubits_in_cat_state + pair_start_index + i])
                                                      for i in range(2)],
                                          measurement_key=measurement_key).get_measurement_circuit()
                    for pair_start_index in range(self._num_qubits_in_cat_state - 1)
                ],
                [
                    X(self.data_qubits[cat_index * self._num_qubits_in_cat_state + i])
                        .with_classical_controls(ParityCheckReader(key=measurement_key, qubit_correction_index=i))
                    for i in range(self._num_qubits_in_cat_state)
                ]
            ])
        return circuit

    def _correct_z_errors(self) -> Circuit:
        circuit = Circuit()
        measurement_key = MeasurementKey(f"THREE_CAT_X_STABILIZER_{uuid4()}")
        for cat_index in range(self.num_cats - 1):
            circuit.append(
                FaultTolerantMeasurer(
                    operations=[X(self.data_qubits[cat_index * self._num_qubits_in_cat_state + i])
                                for i in range(2 * self._num_qubits_in_cat_state)],
                    measurement_key=measurement_key).get_measurement_circuit()
            )
        circuit.append(
            [
                Z(self.data_qubits[cat_index * self._num_qubits_in_cat_state])
                    .with_classical_controls(ParityCheckReader(key=measurement_key, qubit_correction_index=cat_index))
                for cat_index in range(self.num_cats)
            ]
        )
        return circuit

    def _perform_get_operation_circuit(self, operation: LogicalOperation) -> Optional[Circuit]:
        if operation.gate == LogicalGateLabel.X:
            return Circuit(
                [X(self.data_qubits[i]) for i in range(self._num_data_qubits)]
            )
        elif operation.gate == LogicalGateLabel.Z:
            return Circuit(
                [Z(self.data_qubits[i * self._num_qubits_in_cat_state]) for i in range(self.num_cats)],
            )
        return None
