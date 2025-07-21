from dataclasses import dataclass

from cirq import Circuit


@dataclass
class NoisyCircuit:
    circuit: Circuit
    num_noisy_operations: int = 0
