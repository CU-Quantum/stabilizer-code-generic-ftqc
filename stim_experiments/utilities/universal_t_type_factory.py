from stim_experiments.custom_enums.universal_hadamard_type import UniversalHadamardType
from stim_experiments.custom_enums.universal_t_type import UniversalTType
from stim_experiments.error_correcting_codes.support.universal_operations.universal_hadamard.universal_hadamard import UniversalHadamard
from stim_experiments.error_correcting_codes.support.universal_operations.universal_hadamard.universal_hadamard_fault_tolerant_3x import \
    UniversalHadamardFaultTolerant3x
from stim_experiments.error_correcting_codes.support.universal_operations.universal_hadamard.universal_hadamard_single_ancilla import \
    UniversalHadamardSingleAncilla


class UniversalHadamardTypeFactory:
    def __init__(self, t_type: UniversalTType):
        self._t_type = t_type

    def get_universal_hadamard_type(self) -> type[UniversalHadamard]:
        if self._t_type == UniversalHadamardType.FAULT_TOLERANT:
            return UniversalHadamardFaultTolerant3x
        elif self._t_type == UniversalHadamardType.SINGLE_ANCILLA:
            return UniversalHadamardSingleAncilla
        raise ValueError(f"Unknown universal hadamard type: {self._t_type}")
