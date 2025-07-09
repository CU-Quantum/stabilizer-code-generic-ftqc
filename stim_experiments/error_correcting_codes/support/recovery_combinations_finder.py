from collections import defaultdict
from itertools import combinations

import numpy as np

from stim_experiments.custom_dataclasses.recovery import RecoveryGate, RecoveryOperation


class RecoveryCombinationsFinder:
    def __init__(self, max_num_errors: int):
        self._max_num_errors = max_num_errors

    def find_recoveries(self, single_error_recoveries: list[RecoveryGate | RecoveryOperation]) -> dict[tuple[int, ...], list[RecoveryGate | RecoveryOperation]]:
        recovery_gates = defaultdict(list)
        for num_errors in range(1, self._max_num_errors + 1):
            combos = combinations(single_error_recoveries, num_errors)
            for combo in combos:
                symptoms = [recovery_gate.symptom for recovery_gate in combo]
                recovery_gates[tuple(np.sum(symptoms, axis=0))].extend(list(combo))
        return recovery_gates
