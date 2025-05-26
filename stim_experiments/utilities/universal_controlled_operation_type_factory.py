from stim_experiments.custom_enums.universal_controlled_operation_type import UniversalControlledOperationType
from stim_experiments.error_correcting_codes.support.universal_operations.universal_controlled_operation.universal_controlled_operation import \
    UniversalControlledOperation
from stim_experiments.error_correcting_codes.support.universal_operations.universal_controlled_operation.universal_controlled_operation_fault_tolerant import \
    UniversalControlledOperationFaultTolerant
from stim_experiments.error_correcting_codes.support.universal_operations.universal_controlled_operation.universal_controlled_operation_single_ancilla import \
    UniversalControlledOperationSingleAncilla


class UniversalControlledOperationTypeFactory:
    def __init__(self, controlled_operation_type: UniversalControlledOperationType):
        self._controlled_operation_type = controlled_operation_type

    def get_universal_controlled_operation_type(self) -> type[UniversalControlledOperation]:
        if self._controlled_operation_type == UniversalControlledOperationType.FAULT_TOLERANT:
            return UniversalControlledOperationFaultTolerant
        elif self._controlled_operation_type == UniversalControlledOperationType.SINGLE_ANCILLA:
            return UniversalControlledOperationSingleAncilla
        raise ValueError(f"Unknown universal controlled operation type: {self._controlled_operation_type}")
