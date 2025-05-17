from dataclasses import dataclass, field
from typing import Tuple
from uuid import uuid4

import numpy as np
from cirq import ClassicalDataStoreReader, Condition, MeasurementKey
from cirq.protocols import json_serialization
from numpy._typing import NDArray


@dataclass(frozen=True)
class ParityCheckIndexLimit(Condition):
    # TODO test class
    key: MeasurementKey
    parity_check_index: int = 0
    flag_sequence: NDArray[int] = field(default_factory=lambda: np.array([]))

    @property
    def keys(self) -> Tuple[MeasurementKey, ...]:
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
        return self.parity_check_index <= flag_nums_found[0] if len(flag_nums_found) else False

    def _json_dict_(self):
        return json_serialization.dataclass_json_dict(self)

    @classmethod
    def _from_json_dict_(cls, key, parity_check_index, flag_sequence, **kwargs):
        return cls(key=key, parity_check_index=parity_check_index, flag_sequence=flag_sequence)

    @property
    def qasm(self):
        raise ValueError('QASM is defined only for SympyConditions of type key == constant.')
