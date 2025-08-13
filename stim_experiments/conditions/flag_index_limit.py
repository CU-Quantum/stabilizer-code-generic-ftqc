from dataclasses import dataclass
from typing import Tuple

import numpy as np
from cirq import ClassicalDataStoreReader, MeasurementKey, dataclass_json_dict, json_cirq_type
from numpy._typing import NDArray

from stim_experiments.conditions.custom_condition import CustomCondition


@dataclass(frozen=True)
class FlagIndexLimit(CustomCondition):
    key: MeasurementKey
    parity_check_index: int
    flag_sequence: NDArray[int]

    @property
    def keys(self) -> Tuple[MeasurementKey, ...]:
        return (self.key,)

    def replace_key(self, current: MeasurementKey, replacement: MeasurementKey):
        return FlagIndexLimit(replacement, self.parity_check_index, self.flag_sequence) if self.key == current else self

    def __str__(self):
        return str(self.key)

    def __repr__(self):
        return f'{json_cirq_type(type(self))}({self.key!r}, {self.parity_check_index}, {self.flag_sequence})'

    def resolve(self, classical_data: ClassicalDataStoreReader) -> bool:
        if self.key not in classical_data.keys():
            raise ValueError(f'Measurement key "{self.key}" missing when checking flags')
        if not len(self.flag_sequence):
            raise ValueError(f'No flag sequence was given for key "{self.key}"')

        measurements = [x[0] for x in classical_data.records[self.key]]
        if len(measurements) != len(self.flag_sequence[0]):
            raise ValueError(f'Number of measurements for key "{self.key}" ({len(measurements)}) does not match number of flags ({len(self.flag_sequence[0])})')

        flag_nums_found = np.where(np.all(self.flag_sequence == measurements, axis=1))[0]
        return self.parity_check_index <= flag_nums_found[0] if len(flag_nums_found) else False

    def _json_dict_(self):
        return dataclass_json_dict(self)

    @classmethod
    def _from_json_dict_(cls, key, parity_check_index, flag_sequence, **kwargs):
        return cls(key=key, parity_check_index=parity_check_index, flag_sequence=flag_sequence)

    @property
    def qasm(self):
        raise ValueError('QASM is defined only for SympyConditions of type key == constant.')
