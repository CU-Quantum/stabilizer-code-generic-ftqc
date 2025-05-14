from typing import List

from cirq import Circuit, LineQubit, M, MeasurementKey, R, X

from stim_experiments.utilities import FreshAncillasPool


class ParityVerifier:
    def __init__(self, target_qubits: List[LineQubit], measurement_key: MeasurementKey):
        self._target_qubits = target_qubits
        self._measurement_key = measurement_key

    def validate_parity(self) -> Circuit:
        with FreshAncillasPool().use_fresh_ancillas(num_ancillas=1) as ancillas:
            verifier_ancilla = ancillas[0]
            return Circuit(
                    [
                        X(verifier_ancilla).controlled_by(self._target_qubits[i]),
                        X(verifier_ancilla).controlled_by(self._target_qubits[i + 1]),
                        M(verifier_ancilla, key=self._measurement_key),
                        R(verifier_ancilla),
                    ]
                    for i in range(self._num_target_qubits - 1)
            )

    @property
    def _num_target_qubits(self) -> int:
        return len(self._target_qubits)
