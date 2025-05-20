from stim_experiments.custom_enums.universal_hadamard_type import UniversalHadamardType
from stim_experiments.error_correcting_codes.support.universal_hadamard.universal_hadamard import UniversalHadamard
from stim_experiments.error_correcting_codes.support.universal_hadamard.universal_hadamard_fault_tolerant import \
    UniversalHadamardFaultTolerant
from stim_experiments.error_correcting_codes.support.universal_hadamard.universal_hadamard_single_ancilla import \
    UniversalHadamardSingleAncilla


class UniversalHadamardTypeFactory:
    def __init__(self, hadamard_type: UniversalHadamardType):
        self._hadamard_type = hadamard_type

    def get_universal_hadamard_type(self) -> type[UniversalHadamard]:
        if self._hadamard_type == UniversalHadamardType.FAULT_TOLERANT:
            return UniversalHadamardFaultTolerant
        elif self._hadamard_type == UniversalHadamardType.SINGLE_ANCILLA:
            return UniversalHadamardSingleAncilla
        raise ValueError(f"Unknown universal hadamard type: {self._hadamard_type}")
