from dataclasses import dataclass
from typing import Sequence

from cirq import Moment


@dataclass
class NoisyMoment:
    moments: Sequence[Moment]
    num_noisy_operations: int = 0
