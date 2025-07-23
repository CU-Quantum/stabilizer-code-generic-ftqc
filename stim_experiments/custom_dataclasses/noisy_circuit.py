from dataclasses import dataclass, field

from cirq import Circuit

from stim_experiments.custom_dataclasses.noisy_operations_count import NoisyOperationsCount


@dataclass
class NoisyCircuit:
    circuit: Circuit
    noisy_operations_count: NoisyOperationsCount = field(default_factory=NoisyOperationsCount)
