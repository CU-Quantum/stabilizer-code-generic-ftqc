from dataclasses import dataclass


@dataclass
class NoisyOperationsCount:
    one_qubit: int = 0
    two_qubit: int = 0
