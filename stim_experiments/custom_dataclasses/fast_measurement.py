from dataclasses import dataclass, field


@dataclass
class FastMeasurement:
    count: int = 0
    data_qubits: set[int] = field(default_factory=set)
