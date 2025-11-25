from dataclasses import dataclass


@dataclass
class RunConfiguration:
    max_shots: int
    max_errors: int
    depolarization_probabilities: list[float]
    num_workers: int
