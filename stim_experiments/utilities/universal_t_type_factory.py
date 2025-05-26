from stim_experiments.custom_enums.universal_t_type import UniversalTType
from stim_experiments.error_correcting_codes.support.universal_operations.universal_t.universal_t import UniversalT
from stim_experiments.error_correcting_codes.support.universal_operations.universal_t.universal_t_fault_tolerant import \
    UniversalTFaultTolerant
from stim_experiments.error_correcting_codes.support.universal_operations.universal_t.universal_t_singe_ancilla import \
    UniversalTSingleAncilla


class UniversalTTypeFactory:
    def __init__(self, t_type: UniversalTType):
        self._t_type = t_type

    def get_universal_t_type(self) -> type[UniversalT]:
        if self._t_type == UniversalTType.FAULT_TOLERANT:
            return UniversalTFaultTolerant
        elif self._t_type == UniversalTType.SINGLE_ANCILLA:
            return UniversalTSingleAncilla
        raise ValueError(f"Unknown universal T type: {self._t_type}")
