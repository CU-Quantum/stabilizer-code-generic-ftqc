from dataclasses import dataclass, field
from functools import cached_property
from uuid import uuid4

import numpy as np
from cirq import Circuit, ClassicalDataStoreReader, H, KeyCondition, LineQubit, M, MeasurementKey, \
    Operation, R, X, Condition
from cirq.protocols import json_serialization
from numpy._typing import NDArray

from stim_experiments.error_correcting_codes.support.cat_state_creator.support.flag_sequnce_generator import \
    FlagSequenceGenerator
from stim_experiments.utilities import FreshAncillasPool


@dataclass(frozen=True)
class FlagNumLimit(Condition):
    # TODO test class
    key: MeasurementKey
    flag_num: int = 0
    flag_sequence: NDArray[int] = field(default_factory=lambda: array([]))

    @property
    def keys(self):
        return (self.key,)

    def replace_key(self, current: MeasurementKey, replacement: MeasurementKey):
        return KeyCondition(replacement) if self.key == current else self

    def __str__(self):
        return str(self.key)

    def __repr__(self):
        return f'cirq.KeyCondition({self.key!r}, f{self.flag_num})'

    def resolve(self, classical_data: ClassicalDataStoreReader) -> bool:
        if self.key not in classical_data.keys():
            raise ValueError(f'Measurement key {self.key} missing when testing classical control')
        measurements = [x[0] for x in classical_data.records[self.key]]
        if not any(measurements):
            return False
        flag_num_found = np.where(np.all(self.flag_sequence == measurements, axis=1))[0][0]
        return self.flag_num <= flag_num_found

    def _json_dict_(self):
        return json_serialization.dataclass_json_dict(self)

    @classmethod
    def _from_json_dict_(cls, key, **kwargs):
        return cls(key=key)

    @property
    def qasm(self):
        raise ValueError('QASM is defined only for SympyConditions of type key == constant.')


class CatStateCreatorFlagPattern:
    """
    Idea comes from https://quantum-journal.org/papers/q-2023-10-24-1154/
    Note that you apparently cannot use this for syndrome measurement.
    """
    def __init__(self, qubit_register: list[LineQubit]):
        self._qubit_register = qubit_register

    def get_cat_state_circuit(self) -> Circuit:
        if not self._num_data_qubits:
            return Circuit()
        if self._num_data_qubits <= 3:
            return Circuit(
                self._create_cat_state(),
            )
        return Circuit(
            self._create_cat_state(),
            self._measure_flags(),
            self._recover_from_errors(),
        )

    def _create_cat_state(self) -> list[list[Operation]]:
        return [
            [H(self._control_qubit)],
            [X(target_qubit).controlled_by(self._control_qubit) for target_qubit in reversed(self._qubit_register[1:])],
        ]

    def _measure_flags(self) -> list[list[Operation]]:
        with FreshAncillasPool().use_fresh_ancillas(num_ancillas=1) as ancilla_qubits:  # can use single ancilla sequentially for fast measurement
            ancilla = ancilla_qubits[0]
            return [
                X(ancilla).controlled_by(self._control_qubit),
                [
                    [
                        X(ancilla).controlled_by(self._qubit_register[last_seq_num * 3 + 1])
                        for last_seq_num, flags in enumerate(self._flag_sequence[1:])
                        if flags[flag_num] != self._flag_sequence[last_seq_num][flag_num]
                    ] + (self._get_measurement_for_flag(ancilla=ancilla) if flag_num < self._num_measurements - 1 else [])
                    for flag_num in range(self._num_measurements)
                ],
                X(ancilla).controlled_by(self._qubit_register[-1]),
                self._get_measurement_for_flag(ancilla=ancilla),
            ]

    def _get_measurement_for_flag(self, ancilla: LineQubit) -> list[Operation]:
        return [
            M(ancilla, key=self._measurement_key),
            R(ancilla),
        ]

    def _recover_from_errors(self) -> list[list[Operation]]:
        return [
            [X(qubit).with_classical_controls(FlagNumLimit(key=MeasurementKey(self._measurement_key),
                                                           flag_num=flag_num,
                                                           flag_sequence=self._flag_sequence)
                                              )
             for qubit in self._qubit_register[3 * (flag_num -  1):3 * flag_num]]
            for flag_num in range(1, len(self._flag_sequence) - 1)
        ]

    @cached_property
    def _measurement_key(self) -> str:
        return f"CAT_STATE_FLAG_PATTERN_{uuid4().hex}"  # TODO test keys needed, test uuid needed

    @cached_property
    def _flag_sequence(self) -> NDArray[int]:
        return FlagSequenceGenerator(num_flags=self._num_measurements).get_flag_sequence()

    @property
    def _num_measurements(self) -> int:
        arbitrary_measurement_limit = 100
        return next(m for m in range(arbitrary_measurement_limit) if self._num_data_qubits <= 3 * (2 ** m - 2 * m + 2))

    @property
    def _num_data_qubits(self) -> int:
        return len(self._qubit_register)

    @property
    def _control_qubit(self) -> LineQubit:
        return self._qubit_register[0]
