from dataclasses import dataclass

from cirq import LineQubit

from stim_experiments.error_correcting_codes.three_cat_code.three_cat_code import ThreeCatCode
from stim_experiments.error_correcting_codes.three_subregister_parity_code.three_subregister_parity_code import \
    ThreeSubregisterParityCode


@dataclass
class HadamardComputationalLogicalThreeSubregisterParityCodeContext:
    ancilla_qubits: list[LineQubit]
    additional_universal_hadamard_codes: list[ThreeSubregisterParityCode]
    all_subregister_pairity_codes: list[ThreeSubregisterParityCode]
    helper_3cat: ThreeCatCode
