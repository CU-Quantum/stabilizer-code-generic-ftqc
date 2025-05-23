from dataclasses import dataclass

from cirq import Operation

from stim_experiments.custom_dataclasses.universal_hadamard_fault_tolerant_3x_context import \
    UniversalHadamardFaultTolerant3xContext


@dataclass
class UniversalControlledOperationFaultTolerantContext(UniversalHadamardFaultTolerant3xContext):
    target_operations: list[Operation]
