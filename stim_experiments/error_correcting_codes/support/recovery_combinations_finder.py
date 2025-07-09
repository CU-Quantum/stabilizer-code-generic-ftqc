from collections import defaultdict
from dataclasses import replace
from itertools import combinations
from typing import Optional

import numpy as np
from cirq import X, Y, Z

from stim_experiments.custom_dataclasses.recovery import RecoveryGate, RecoveryOperation


class RecoveryCombinationsFinder:
    def __init__(self, max_num_errors: Optional[int] = None, max_num_x_errors: Optional[int] = None, max_num_z_errors: Optional[int] = None):
        self._max_num_errors = max_num_errors
        self._max_num_x_errors = max_num_x_errors
        self._max_num_z_errors = max_num_z_errors

    def find_recoveries(self, single_error_recoveries: list[RecoveryGate | RecoveryOperation]) -> list[RecoveryGate | RecoveryOperation]:
        self._validate()
        recovery_gates = []
        for num_errors in range(1, self._max_num_errors + 1):
            combos = combinations(single_error_recoveries, num_errors)
            for combo in combos:
                symptoms = [recovery_gate.symptom for recovery_gate in combo]
                symptoms_combined = np.mod(np.sum(symptoms, axis=0), 2).tolist()

                error_types = [recovery_gate.gate for recovery_gate in combo]
                y_errors = error_types.count(Y)
                x_is_below_limit = error_types.count(X) + y_errors <= self._max_num_x_errors
                z_is_below_limit = error_types.count(Z) + y_errors <= self._max_num_z_errors
                if x_is_below_limit and z_is_below_limit:
                    for recovery_gate in combo:
                        recovery_gates.append(replace(recovery_gate, symptom=symptoms_combined))
        return recovery_gates

    def _validate(self) -> None:  # TODO test this
        if self._max_num_errors is None and (self._max_num_x_errors is None or self._max_num_z_errors is None):
            raise ValueError(
                'Either "max_num_errors" must be provided or both "max_num_x_errors" and "max_num_z_errors" must be provided.'
            )

        if self._max_num_errors is None:
            self._max_num_errors = self._max_num_x_errors + self._max_num_z_errors
        if self._max_num_x_errors is None:
            self._max_num_x_errors = self._max_num_errors
        if self._max_num_z_errors is None:
            self._max_num_z_errors = self._max_num_errors
