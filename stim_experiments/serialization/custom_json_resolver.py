from typing import Optional

import sympy
from cirq import DEFAULT_RESOLVERS, JsonResolver
from cirq.protocols.json_serialization import ObjectFactory, ObjectHook

from stim_experiments import conditions
from stim_experiments.utilities.circuit_operation_hacks import get_hacked_circuit_operation
from stim_experiments.conditions import MajorityVote
from stim_experiments.utilities.measurement_key_with_stable_hash import MeasurementKeyWithStableHash


class CustomJsonResolver(JsonResolver):
    def circuit_operation_factory(self, *args, **kwargs):
        majority_vote = kwargs.get('repeat_until')
        if isinstance(majority_vote, MajorityVote):
            subcircuit = kwargs.get('circuit')
            get_hacked_circuit_operation(subcircuit=subcircuit, majority_vote=majority_vote)
        return ObjectHook(resolvers=DEFAULT_RESOLVERS)({**kwargs, 'cirq_type': 'CircuitOperation'})

    def __call__(self, cirq_type: str) -> Optional[ObjectFactory]:
        if 'stim_experiments.conditions' in cirq_type:
            return getattr(conditions, cirq_type.split('.')[-1])
        return {
            'CircuitOperation': self.circuit_operation_factory,
            'stim_experiments.utilities.measurement_key_with_stable_hash.MeasurementKeyWithStableHash': MeasurementKeyWithStableHash,
            'sympy.And': sympy.And,
        }.get(cirq_type, None)
