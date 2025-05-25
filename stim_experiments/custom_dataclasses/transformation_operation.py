from dataclasses import dataclass
from enum import Enum, auto
from typing import Optional


class TransformationGate(Enum):
    CX = auto()
    CZ = auto()
    H = auto()
    M = auto()
    X = auto()
    Z = auto()


@dataclass
class TransformationOperation:
    gate: TransformationGate
    target_qubit_index: int
    control_qubit_index: Optional[int] = None

    def validate(self) -> None:
        is_double_qubit = self.gate in (TransformationGate.CX, TransformationGate.CZ)
        if is_double_qubit and self.control_qubit_index is None:
            raise ValueError(f"Double-qubit gates must have a control qubit. "
                             f"Was not given a control index "
                             f"for a(n) {self.gate.name} gate.")
        if not is_double_qubit and self.control_qubit_index is not None:
            raise ValueError(f"Single-qubit gates may have only a target qubit. "
                             f"Was given control index {self.control_qubit_index} "
                             f"for a(n) {self.gate.name} gate.")
