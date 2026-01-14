from functools import partial

from cirq import Circuit, CircuitOperation, FrozenCircuit, MeasurementKey

from cirq_experiments.conditions import MajorityVote


def hack_to_add_desired_key_to_list_of_modified_keys(subcircuit: FrozenCircuit, majority_vote: MajorityVote) -> None:
    measurement_keys = set(subcircuit._measurement_key_objs_())
    measurement_keys.add(majority_vote.key)
    subcircuit.unfreeze = partial(unfreeze_hacked, measurement_keys=measurement_keys, unfreeze_unhacked=subcircuit.unfreeze)


def unfreeze_hacked(copy: bool = True, measurement_keys: set = None, unfreeze_unhacked: callable = None) -> Circuit:
    unfrozen = unfreeze_unhacked(copy=copy)
    unfrozen._with_rescoped_keys_ = partial(with_rescoped_keys_hacked, measurement_keys=measurement_keys, with_rescoped_keys_unhacked=unfrozen._with_rescoped_keys_)
    return unfrozen


def with_rescoped_keys_hacked(path: tuple[str, ...],
                              bindable_keys: frozenset[MeasurementKey],
                              measurement_keys: set[MeasurementKey],
                              with_rescoped_keys_unhacked: callable,
                              ):
    unmodified = with_rescoped_keys_unhacked(path, bindable_keys)
    unmodified._measurement_key_objs_ = lambda: frozenset(measurement_keys)
    return unmodified


def replace_hacked(majority_vote: MajorityVote, replace_unhacked: callable, **changes) -> CircuitOperation:
        subcircuit = changes['circuit']
        hack_to_add_desired_key_to_list_of_modified_keys(subcircuit, majority_vote)
        return replace_unhacked(**changes)
