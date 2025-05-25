from dataclasses import dataclass
from typing import List

from cirq import Gate, Operation


@dataclass
class RecoveryGates:
    gate: Gate
    qubit_index: int
    symptom: List[int]


@dataclass
class RecoveryOperations:
    operation: Operation
    symptom: List[int]
