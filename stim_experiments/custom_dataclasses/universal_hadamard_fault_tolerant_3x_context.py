from dataclasses import dataclass

from cirq import Operation

from stim_experiments.custom_dataclasses.universal_operations_context import UniversalOperationsContext


@dataclass
class UniversalHadamardFaultTolerant3xContext(UniversalOperationsContext):
    data_code_logical_x: list[Operation]
    data_code_logical_z: list[Operation]
