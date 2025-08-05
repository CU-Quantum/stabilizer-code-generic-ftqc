from dataclasses import dataclass, field


@dataclass
class NoisyOperationsCount:
    x_errors: int = 0
    z_errors: int = 0
    y_errors: int = 0
    one_qubit: int = 0
    two_qubit: int = 0

    def modify(self, other: 'NoisyOperationsCount') -> None:
        self.x_errors += other.x_errors
        self.z_errors += other.z_errors
        self.y_errors += other.y_errors
        self.one_qubit += other.one_qubit
        self.two_qubit += other.two_qubit


@dataclass
class NoisyOperationsCountPerGate:
    count: list[NoisyOperationsCount] = field(default_factory=lambda: [NoisyOperationsCount()])

    def append_count(self) -> None:
        self.count.append(NoisyOperationsCount())

    def add_count_to_latest(self, operand: NoisyOperationsCount) -> None:
        self.count[-1].modify(operand)

    def extend(self, new_counts: list[NoisyOperationsCount]) -> None:
        self.count.extend(new_counts)

    @property
    def first_count(self) -> NoisyOperationsCount:
        return self.count[0]

    @property
    def latest_count(self) -> NoisyOperationsCount:
        return self.count[-1]

    @property
    def tail(self) -> list[NoisyOperationsCount]:
        return self.count[1:]
