from dataclasses import dataclass

from cirq import Operation

from stim_experiments.custom_dataclasses.universal_hadamard_fault_tolerant_context import \
    UniversalHadamardFaultTolerantContext


@dataclass
class UniversalControlledOperationFaultTolerantContext(UniversalHadamardFaultTolerantContext):
    target_operations: list[Operation]
