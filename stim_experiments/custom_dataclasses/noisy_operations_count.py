from dataclasses import asdict, dataclass, field


@dataclass
class NoisyOperationsCountPerShot:
    i_errors: int = 0
    x_errors: int = 0
    z_errors: int = 0
    y_errors: int = 0
    one_qubit: int = 0
    two_qubit: int = 0

    @property
    def num_non_identity(self) -> int:
        return self.x_errors + self.y_errors + self.z_errors

    def modify(self, other: 'NoisyOperationsCountPerShot') -> None:
        self.i_errors += other.i_errors
        self.x_errors += other.x_errors
        self.z_errors += other.z_errors
        self.y_errors += other.y_errors
        self.one_qubit += other.one_qubit
        self.two_qubit += other.two_qubit

    def reset(self) -> None:
        self.i_errors = 0
        self.x_errors = 0
        self.z_errors = 0
        self.y_errors = 0
        self.one_qubit = 0
        self.two_qubit = 0


@dataclass
class NoisyOperationsCountPerCorrectionRound:
    count: list[list[NoisyOperationsCountPerShot]] = field(default_factory=lambda: [[NoisyOperationsCountPerShot()]])

    def append_correction_round(self) -> None:
        self.count.append([NoisyOperationsCountPerShot()])

    def append_shot(self) -> None:
        for count in self.count:
            count.insert(-1, NoisyOperationsCountPerShot(**asdict(count[-1])))
            count[-1].reset()

    def add_count_to_latest(self, operand: NoisyOperationsCountPerShot) -> None:
        self.count[-1][-1].modify(operand)

    def extend(self, new_counts: list[list[NoisyOperationsCountPerShot]]) -> None:
        self.count.extend(new_counts)

    @property
    def first_count(self) -> NoisyOperationsCountPerShot:
        return self.count[0][-1]

    @property
    def latest_count(self) -> NoisyOperationsCountPerShot:
        return self.count[-1][-1]

    @property
    def tail(self) -> list[list[NoisyOperationsCountPerShot]]:
        return self.count[1:]
