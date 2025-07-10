import numpy
import pytest
from cirq import Circuit, CircuitOperation, ClassicalDataDictionaryStore, FrozenCircuit, LineQubit, M, Simulator

from stim_experiments.conditions.majority_vote import \
    MajorityVote


class MajorityVoteStub(MajorityVote):
    def __init__(self, desired_measurement_key: str):
        super().__init__(desired_measurement_key=desired_measurement_key)
        self.saved_measurements = []

    def resolve(self, classical_data: ClassicalDataDictionaryStore) -> bool:
        self.saved_measurements = self._get_measurements(classical_data=classical_data)
        return True


class TestThreeRepetitionsMajorityVote:
    def test_measurements_are_separate_per_instance(self):
        separate_condition_instances = [MajorityVoteStub(desired_measurement_key='foo') for _ in range(2)]
        qubits = LineQubit.range(1)
        circuit = Circuit(
            CircuitOperation(
                FrozenCircuit(
                    M(qubits[0], key=condition.key)
                ),
                use_repetition_ids=False,
                repeat_until=condition
            ) for condition in separate_condition_instances
        )
        Simulator().simulate(circuit)
        assert all(len(separate_condition_instance.saved_measurements) == 1 for separate_condition_instance in separate_condition_instances)

    def test_missing_key(self):
        store = ClassicalDataDictionaryStore()
        condition = MajorityVote(desired_measurement_key='foo')
        with pytest.raises(ValueError, match=f'^Measurement key {condition.key} missing when majority voting\\.$'):
            condition.resolve(classical_data=store)

    def test_stores_majority_vote_into_desired_key(self):
        numpy.random.seed(0)

        store = ClassicalDataDictionaryStore()
        desired_key = 'foo'
        condition = MajorityVote(desired_measurement_key=desired_key)
        different_measurements = [0, 1, 0]
        for i in range(condition.number_of_votes):
            is_last_vote = i == condition.number_of_votes - 1
            store.record_measurement(key=condition.key, measurement=(different_measurements[i],), qubits=(LineQubit(0),))
            assert condition.resolve(store) == is_last_vote
        assert store.records[desired_key] == [(0,)]
