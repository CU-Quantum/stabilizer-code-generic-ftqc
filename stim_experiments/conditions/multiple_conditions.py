from cirq import ClassicalDataDictionaryStore, Condition, MeasurementKey


class MultipleConditions(Condition):
    def __init__(self, conditions: list[Condition]):
        self._conditions = conditions

    @property
    def keys(self):
        return tuple(key for condition in self._conditions for key in condition.keys)

    def replace_key(self, current: MeasurementKey, replacement: MeasurementKey):
        for condition in self._conditions:
            if current in condition.keys:
                condition.replace_key(current, replacement)
        return self

    def __str__(self):
        return str(self.keys)

    def __repr__(self):
        return f'MultipleConditions({self.keys!r})'

    def resolve(self, classical_data: ClassicalDataDictionaryStore) -> bool:
        return all(condition.resolve(classical_data=classical_data) for condition in self._conditions)

    @property
    def qasm(self):
        raise ValueError('QASM is defined only for SympyConditions of type key == constant.')
