from dataclasses import dataclass

from cirq import LineQubit

from stim_experiments.error_correcting_codes.three_cat_code.three_cat_code import ThreeCatCode
from stim_experiments.error_correcting_codes.cat_parity_code.cat_parity_code import \
    CatParityCode


@dataclass
class HadamardComputationalLogicalThreeSubregisterParityCodeContext:
    ancilla_qubits: list[LineQubit]
    additional_universal_hadamard_codes: list[CatParityCode]
    all_subregister_pairity_codes: list[CatParityCode]
    helper_3cat: ThreeCatCode
