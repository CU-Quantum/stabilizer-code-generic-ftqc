from dataclasses import dataclass


@dataclass
class NoiseParameters:
    depolarization_probability_one_qubit: float
    depolarization_probability_two_qubit: float
