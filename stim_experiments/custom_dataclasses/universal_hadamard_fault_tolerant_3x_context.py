from dataclasses import dataclass

from cirq import LineQubit, Operation

from stim_experiments.error_correcting_codes.three_cat_code.three_cat_code import ThreeCatCode
from stim_experiments.error_correcting_codes.three_subregister_parity_code.three_subregister_parity_code import \
    ThreeSubregisterParityCode
from stim_experiments.error_correcting_codes.universal_hadamard_helper_code.universal_hadamard_helper_code import \
    UniversalHadamardHelperCode


@dataclass
class UniversalHadamardFaultTolerant3xContext:
    ancilla_qubits: list[LineQubit]
    data_code_logical_x: list[Operation]
    data_code_logical_z: list[Operation]
    three_subregister_parity_code: ThreeSubregisterParityCode
    three_cat: ThreeCatCode
    universal_hadamard_helper_code: UniversalHadamardHelperCode
