from dataclasses import dataclass, field


@dataclass
class NoisyOperationsCount:
    count: int = 0
    paths: list[list[int]] = field(default_factory=list)

    def modify(self, other):
        self.count += other.count
        self.paths.extend(other.paths)


@dataclass
class NoisyOperationsCountPerShot:
    i_errors: NoisyOperationsCount = field(default_factory=NoisyOperationsCount)
    x_errors: NoisyOperationsCount = field(default_factory=NoisyOperationsCount)
    z_errors: NoisyOperationsCount = field(default_factory=NoisyOperationsCount)
    y_errors: NoisyOperationsCount = field(default_factory=NoisyOperationsCount)
    one_qubit: int = 0
    two_qubit: int = 0

    def reset(self) -> None:
        self.i_errors = NoisyOperationsCount()
        self.x_errors = NoisyOperationsCount()
        self.z_errors = NoisyOperationsCount()
        self.y_errors = NoisyOperationsCount()
        self.one_qubit = 0
        self.two_qubit = 0

    @property
    def num_non_identity_errors(self) -> int:
        return self.x_errors.count + self.y_errors.count + self.z_errors.count

    def modify(self, other: 'NoisyOperationsCountPerShot') -> None:
        self.i_errors.modify(other.i_errors)
        self.x_errors.modify(other.x_errors)
        self.z_errors.modify(other.z_errors)
        self.y_errors.modify(other.y_errors)
        self.one_qubit += other.one_qubit
        self.two_qubit += other.two_qubit


@dataclass
class NoisyOperationsCountPerCorrectionRound:
    counts: list[NoisyOperationsCountPerShot] = field(default_factory=lambda: [NoisyOperationsCountPerShot()])

    def append_correction_round(self) -> None:
        self.counts.append(NoisyOperationsCountPerShot())

    def add_count_to_latest(self, operand: NoisyOperationsCountPerShot) -> None:
        self.counts[-1].modify(operand)

    def extend(self, new_counts: list[NoisyOperationsCountPerShot]) -> None:
        self.counts.extend(new_counts)

    @property
    def first_count(self) -> NoisyOperationsCountPerShot:
        return self.counts[0]

    @property
    def latest_count(self) -> NoisyOperationsCountPerShot:
        return self.counts[-1]

    @property
    def num_non_identity_errors(self) -> int:
        return sum(count.num_non_identity_errors for count in self.counts)

    @property
    def tail(self) -> list[NoisyOperationsCountPerShot]:
        return self.counts[1:]
