from dataclasses import dataclass


@dataclass
class NoisyOperationsCount:
    x_errors: int = 0
    z_errors: int = 0
    y_errors: int = 0
    one_qubit: int = 0
    two_qubit: int = 0
