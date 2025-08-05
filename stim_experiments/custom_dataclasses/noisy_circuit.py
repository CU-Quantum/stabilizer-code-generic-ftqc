from dataclasses import dataclass, field

from cirq import Circuit

from stim_experiments.custom_dataclasses.noisy_operations_count import NoisyOperationsCountPerCorrectionRound


@dataclass
class NoisyCircuit:
    circuit: Circuit
    noisy_operations_count: NoisyOperationsCountPerCorrectionRound = field(default_factory=NoisyOperationsCountPerCorrectionRound)
