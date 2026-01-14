from dataclasses import dataclass

from cirq import LineQubit

from cirq_experiments.error_correcting_codes.generalized_shor_code_hadamard.generalized_shor_code_hadamard import \
    GeneralizedShorCodeHadamard
from cirq_experiments.error_correcting_codes.generalized_shor_code.generalized_shor_code import GeneralizedShorCode


@dataclass
class UniversalOperationsContext:
    ancilla_qubits: list[LineQubit]
    cat_parity_code: GeneralizedShorCodeHadamard
    multiple_cat_code: GeneralizedShorCode
