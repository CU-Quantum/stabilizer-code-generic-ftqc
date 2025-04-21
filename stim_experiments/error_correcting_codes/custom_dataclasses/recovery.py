from dataclasses import dataclass
from typing import List

from cirq import Gate


@dataclass
class Recovery:
    gate: Gate
    qubit_index: int
    symptom: List[int]
