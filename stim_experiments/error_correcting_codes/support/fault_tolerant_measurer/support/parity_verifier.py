from typing import List, Optional

from cirq import Circuit, LineQubit, M, R, X

from stim_experiments.error_correcting_codes.support.fault_tolerant_measurer.support.conditions.verification_is_zero import \
    VerificationIsZero


class ParityVerifier:
    def __init__(self,
                 target_qubits: List[LineQubit],
                 verifier_ancilla: Optional[LineQubit] = None):
        self._target_qubits = target_qubits
        self._verifier_ancilla = verifier_ancilla

    def validate_parity(self) -> Circuit:
        return Circuit(
                [
                    X(self._verifier_ancilla).controlled_by(self._target_qubits[i]),
                    X(self._verifier_ancilla).controlled_by(self._target_qubits[i + 1]),
                    M(self._verifier_ancilla, key=VerificationIsZero().key),
                    R(self._verifier_ancilla),
                ]
                for i in range(self._num_target_qubits - 1)
        )

    @property
    def _num_target_qubits(self) -> int:
        return len(self._target_qubits)
