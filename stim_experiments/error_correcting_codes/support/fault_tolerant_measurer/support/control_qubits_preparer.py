from cirq import Circuit, CircuitOperation, LineQubit, R

from stim_experiments.error_correcting_codes.support.fault_tolerant_measurer.support.conditions.verification_is_zero import \
    VerificationIsZero
from stim_experiments.error_correcting_codes.support.fault_tolerant_measurer.support.parity_verifier import \
    ParityVerifier
from stim_experiments.error_correcting_codes.support.fault_tolerant_measurer.support.cat_state_circuit_creator import \
    CatStateCircuitCreator


class ControlQubitsPreparer:
    def __init__(self, target_qubits: list[LineQubit], verifier_ancilla: LineQubit):
        self._target_qubits = target_qubits
        self._verifier_ancilla = verifier_ancilla

    def prepare_state(self) -> Circuit:
        preparation_circuit = Circuit(
            [R(qubit) for qubit in self._target_qubits + [self._verifier_ancilla]],
            CatStateCircuitCreator(target_qubits=self._target_qubits).create_circuit(),
            ParityVerifier(target_qubits=self._target_qubits, verifier_ancilla=self._verifier_ancilla).validate_parity(),
        )
        repeat_until = VerificationIsZero() if len(self._target_qubits) > 1 else None
        return Circuit(
            CircuitOperation(preparation_circuit.freeze(), use_repetition_ids=False, repeat_until=repeat_until),
        )
