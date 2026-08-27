from dataclasses import dataclass

from cirq import LineQubit

from cirq_experiments.error_correcting_codes.generalized_shor_code_x_basis.generalized_shor_code_x_basis import \
    GeneralizedShorCodeXBasis
from cirq_experiments.error_correcting_codes.generalized_shor_code.generalized_shor_code import GeneralizedShorCode


@dataclass
class UniversalOperationsContext:
    ancilla_qubits: list[LineQubit]
    cat_parity_code: GeneralizedShorCodeXBasis
    multiple_cat_code: GeneralizedShorCode
