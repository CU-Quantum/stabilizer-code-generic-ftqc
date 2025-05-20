from dataclasses import dataclass

from cirq import LineQubit

from stim_experiments.error_correcting_codes.three_cat_code.three_cat_code import ThreeCatCode
from stim_experiments.error_correcting_codes.three_cat_subregister_parity_code.three_cat_subregister_parity_code import \
    ThreeCatSubregisterParityCode


@dataclass
class HadamardComputationalLogicalThreeSubregisterParityCodeContext:
    ancilla_qubits: list[LineQubit]
    additional_universal_hadamard_codes: list[ThreeCatSubregisterParityCode]
    all_universal_hadamard_codes: list[ThreeCatSubregisterParityCode]
    helper_3cat: ThreeCatCode
