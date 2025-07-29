from dataclasses import dataclass

from cirq import LineQubit

from stim_experiments.error_correcting_codes.cat_parity_code.cat_parity_code import \
    CatParityCode
from stim_experiments.error_correcting_codes.multiple_cat_code.multiple_cat_code import MultipleCatCode


@dataclass
class UniversalOperationsContext:
    ancilla_qubits: list[LineQubit]
    cat_parity_code: CatParityCode
    multiple_cat_code: MultipleCatCode
