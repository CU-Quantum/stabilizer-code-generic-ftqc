from dataclasses import dataclass
from enum import Enum, auto
from typing import List


class LogicalGateLabel(Enum):
    X = auto()
    Z = auto()
    H = auto()


@dataclass
class LogicalOperation:
    gate: LogicalGateLabel
    qubit_index: int
