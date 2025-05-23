from dataclasses import dataclass

from cirq import LineQubit, Operation

from stim_experiments.custom_dataclasses.universal_operations_context import UniversalOperationsContext
from stim_experiments.error_correcting_codes.three_cat_code.three_cat_code import ThreeCatCode
from stim_experiments.error_correcting_codes.three_subregister_parity_code.three_subregister_parity_code import \
    ThreeSubregisterParityCode
from stim_experiments.error_correcting_codes.universal_hadamard_helper_code.universal_hadamard_helper_code import \
    UniversalHadamardHelperCode


@dataclass
class UniversalHadamardFaultTolerant3xContext(UniversalOperationsContext):
    data_code_logical_x: list[Operation]
    data_code_logical_z: list[Operation]
