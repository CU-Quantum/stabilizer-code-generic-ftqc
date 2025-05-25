from dataclasses import dataclass

from cirq import LineQubit, Operation

from stim_experiments.error_correcting_codes.three_cat_code.three_cat_code import ThreeCatCode
from stim_experiments.error_correcting_codes.cat_parity_code.cat_parity_code import \
    CatParityCode


@dataclass
class UniversalOperationsContext:
    ancilla_qubits: list[LineQubit]
    cat_parity_code: CatParityCode
    three_cat: ThreeCatCode
