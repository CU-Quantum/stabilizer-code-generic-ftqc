from cirq import LineQubit

from stim_experiments.custom_dataclasses.check_matrix import CheckMatrix
from stim_experiments.custom_dataclasses.recovery import RecoveryOperations
from stim_experiments.error_correcting_codes.support.recovery_finder import RecoveryFinder


class RecoveryOperationsFinder:
    def __init__(self, check_matrix: CheckMatrix, qubits: list[LineQubit]):
        self._check_matrix = check_matrix
        self._qubits = qubits

    def find_recovery_operations(self):
        recoveries = RecoveryFinder(check_matrix=self._check_matrix).find_recoveries()
        return [
            RecoveryOperations(
                operation=recovery_gates.gate(self._qubits[recovery_gates.qubit_index]),
                symptom=recovery_gates.symptom
            )
            for recovery_gates in recoveries
        ]
