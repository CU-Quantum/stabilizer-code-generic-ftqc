from dataclasses import dataclass, field
from functools import cached_property
from typing import Optional
from uuid import uuid4

import numpy as np
from cirq import Circuit, ClassicalDataStoreReader, H, LineQubit, M, MeasurementKey, \
    Operation, R, X, Condition
from cirq.protocols import json_serialization
from numpy import array
from numpy._typing import NDArray
from numpy.ma.extras import average

from stim_experiments.error_correcting_codes.support.cat_state_creator.support.flag_sequnce_generator import \
    FlagSequenceGenerator
from stim_experiments.utilities import FreshAncillasPool

@dataclass
class ParityCheckInfo:
    control_qubit_index: int
    recovery_qubit_num: Optional[int] = None
    flags_outcome: NDArray[int] = field(default_factory=lambda: array([]))


@dataclass(frozen=True)
class ParityCheckIndexLimit(Condition):
    # TODO test class
    key: MeasurementKey
    parity_check_index: int = 0
    flag_sequence: NDArray[int] = field(default_factory=lambda: array([]))

    @property
    def keys(self):
        return (self.key,)

    def replace_key(self, current: MeasurementKey, replacement: MeasurementKey):
        return ParityCheckIndexLimit(replacement, self.parity_check_index, self.flag_sequence) if self.key == current else self

    def __str__(self):
        return str(self.key)

    def __repr__(self):
        return f'ParityCheckIndexLimit({self.key!r}, f{self.parity_check_index})'

    def resolve(self, classical_data: ClassicalDataStoreReader) -> bool:
        if self.key not in classical_data.keys():
            raise ValueError(f'Measurement key {self.key} missing when checking flags')
        measurements = [x[0] for x in classical_data.records[self.key]]
        flag_nums_found = np.where(np.all(self.flag_sequence == measurements, axis=1))[0]
        return self.parity_check_index <= flag_nums_found[0] if flag_nums_found else False

    def _json_dict_(self):
        return json_serialization.dataclass_json_dict(self)

    @classmethod
    def _from_json_dict_(cls, key, parity_check_index, flag_sequence, **kwargs):
        return cls(key=key, parity_check_index=parity_check_index, flag_sequence=flag_sequence)

    @property
    def qasm(self):
        raise ValueError('QASM is defined only for SympyConditions of type key == constant.')


class CatStateCreatorFlagPattern:
    # TODO clean this up
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
            self.correct_errors(),
        )

    def _create_cat_state(self) -> list[list[Operation]]:
        return [
            [H(self._control_qubit)],
            [X(target_qubit).controlled_by(self._control_qubit) for target_qubit in reversed(self._qubit_register[1:])],
        ]

    def correct_errors(self) -> Circuit:
        if not self._num_data_qubits or self._num_data_qubits <= 3:
            return Circuit()
        return Circuit(
            self._measure_flags(),
            self._recover_from_errors(),
        )

    def _measure_flags(self) -> list[list[Operation]]:
        with FreshAncillasPool().use_fresh_ancillas(num_ancillas=1) as ancilla_qubits:
            ancilla = ancilla_qubits[0]
            return [
                X(ancilla).controlled_by(self._qubit_register[self._parity_check_infos[0].control_qubit_index]),
                [
                    [
                        X(ancilla).controlled_by(self._qubit_register[parity_check_info.control_qubit_index])
                        for previous_parity_check_index, parity_check_info in enumerate(self._parity_check_infos[1:-1])
                        if parity_check_info.flags_outcome[flag_index]
                           != self._parity_check_infos[previous_parity_check_index].flags_outcome[flag_index]
                    ] + (self._get_measurement(ancilla=ancilla) if flag_index < self._num_measurements - 1 else [])
                    for flag_index in range(self._num_measurements)
                ],
                X(ancilla).controlled_by(self._qubit_register[self._parity_check_infos[-1].control_qubit_index]),
                self._get_measurement(ancilla=ancilla),
            ]

    def _get_measurement(self, ancilla: LineQubit) -> list[Operation]:
        return [
            M(ancilla, key=self._measurement_key),
            R(ancilla),
        ]

    def _recover_from_errors(self) -> list[list[Operation]]:
        return [
            [X(qubit).with_classical_controls(ParityCheckIndexLimit(key=MeasurementKey(self._measurement_key),
                                                                    parity_check_index=parity_check_index - 1,
                                                                    flag_sequence=self._flag_sequence)
                                              )
             for qubit in self._qubit_register[self._parity_check_infos[parity_check_index - 1].recovery_qubit_num:self._parity_check_infos[parity_check_index].recovery_qubit_num]]
            for parity_check_index in range(2, len(self._parity_check_infos) - 1)
        ]

    @cached_property
    def _measurement_key(self) -> str:
        return f"CAT_STATE_FLAG_PATTERN_{uuid4().hex}"  # TODO test keys needed, test uuid needed

    @cached_property
    def _parity_check_infos(self) -> list[ParityCheckInfo]:
        perfect_num_data_qubits = 3 * (2 ** self._num_measurements - 2 * self._num_measurements + 2)
        num_data_qubits_less_than_perfect = perfect_num_data_qubits - self._num_data_qubits
        initial_flag = ParityCheckInfo(control_qubit_index=0,
                                       flags_outcome=self._flag_sequence[0])
        last_flag = ParityCheckInfo(control_qubit_index=perfect_num_data_qubits - 1)
        parity_check_data = ([initial_flag]
                           + [ParityCheckInfo(control_qubit_index=last_seq_num * 3 + 1,
                                              recovery_qubit_num=3 * last_seq_num,
                                              flags_outcome=flags_outcome)
                              for last_seq_num, flags_outcome in enumerate(self._flag_sequence[1:])]
                           + [last_flag])
        for i in range(num_data_qubits_less_than_perfect):
            measurement_num_to_move = next(parity_check_index for parity_check_index in range(len(parity_check_data) - 2, 1, -1)
                 if parity_check_data[parity_check_index].control_qubit_index - 1 > parity_check_data[parity_check_index - 1].control_qubit_index)
            for j in range(measurement_num_to_move, len(parity_check_data)):
                parity_check_data[j].control_qubit_index -= 1
                parity_check_data[j].recovery_qubit_num = int(np.floor(average([parity_check_data[j - 1].control_qubit_index, parity_check_data[j].control_qubit_index]))) + 1
        return parity_check_data

    @cached_property
    def _flag_sequence(self) -> NDArray[NDArray[int]]:
        return FlagSequenceGenerator(num_flags=self._num_measurements).get_flag_sequence()

    @property
    def _control_qubit(self) -> LineQubit:
        return self._qubit_register[0]

    @cached_property
    def _num_measurements(self) -> int:
        arbitrary_measurement_limit = 100
        return next(m for m in range(2, arbitrary_measurement_limit) if self._num_data_qubits <= 3 * (2 ** m - 2 * m + 2))

    @property
    def _num_data_qubits(self) -> int:
        return len(self._qubit_register)
