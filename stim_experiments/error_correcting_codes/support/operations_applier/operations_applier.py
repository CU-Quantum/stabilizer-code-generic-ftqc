from abc import ABC, abstractmethod
from typing import Optional

from cirq import Circuit, Condition, Operation
from sympy import Expr


class OperationsApplier(ABC):
    def __init__(self,
                 operations: list[Operation],
                 condition: Optional[Condition | Expr] = None,
                 ):
        self._operations = operations
        self._condition = condition

    @abstractmethod
    def get_application_circuit(self) -> Circuit:
        pass
