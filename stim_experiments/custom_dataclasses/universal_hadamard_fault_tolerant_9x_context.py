from dataclasses import dataclass

from cirq import LineQubit, Operation

from stim_experiments.error_correcting_codes.three_cat_code.three_cat_code import ThreeCatCode
from stim_experiments.error_correcting_codes.cat_parity_code.cat_parity_code import \
    CatParityCode


@dataclass
class UniversalHadamardFaultTolerant9xContext:
    ancilla_qubits: list[LineQubit]
    three_subregister_parity_codes_small: list[CatParityCode]
    three_subregister_parity_code_large: CatParityCode
    three_cat_small: ThreeCatCode
    three_cat_large: ThreeCatCode
    data_code_logical_x: list[Operation]
    data_code_logical_z: list[Operation]
