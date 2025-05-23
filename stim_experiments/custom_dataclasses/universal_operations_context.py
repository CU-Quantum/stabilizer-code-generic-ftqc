from dataclasses import dataclass

from cirq import LineQubit, Operation

from stim_experiments.error_correcting_codes.three_cat_code.three_cat_code import ThreeCatCode
from stim_experiments.error_correcting_codes.three_subregister_parity_code.three_subregister_parity_code import \
    ThreeSubregisterParityCode


@dataclass
class UniversalOperationsContext:
    ancilla_qubits: list[LineQubit]
    three_subregister_parity_code: ThreeSubregisterParityCode
    three_cat: ThreeCatCode
