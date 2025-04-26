from functools import cached_property
from typing import Optional

from cirq import Circuit, CircuitOperation, LineQubit, R, inverse

from stim_experiments.error_correcting_codes.support.fault_tolerant_measurer.support.conditions.verification_is_zero import \
    VerificationIsZero
from stim_experiments.error_correcting_codes.support.fault_tolerant_measurer.support.parity_verifier import \
    ParityVerifier
from stim_experiments.error_correcting_codes.support.fault_tolerant_measurer.support.cat_state_circuit_creator import \
    StatePropagator


class StatePropagationParityEnsurer:
    # TODO test class
    def __init__(self,
                 target_qubits: list[LineQubit],
                 verifier_ancilla: Optional[LineQubit],
                 first_qubit_preparer: Circuit,
                 ):
        self.target_qubits = target_qubits
        self._verifier_ancilla = verifier_ancilla
        self._first_qubit_preparer = first_qubit_preparer

    def prepare_state(self) -> Circuit:
        # TODO ensure verifier ancilla is not in target qubits
        # TODO ensure verifier ancilla exists if target qubits is greater than 1
        all_qubits = self.target_qubits.copy()
        if self._verifier_ancilla:
            all_qubits.append(self._verifier_ancilla)
        preparation_circuit = Circuit(
            [R(qubit) for qubit in all_qubits],
            self._state_propagation,
            ParityVerifier(target_qubits=self.target_qubits,
                           verifier_ancilla=self._verifier_ancilla).validate_parity(),
        )
        repeat_until = VerificationIsZero() if len(self.target_qubits) > 1 else None
        return Circuit(
            CircuitOperation(preparation_circuit.freeze(), use_repetition_ids=False, repeat_until=repeat_until),
        )

    def decode_state(self) -> Circuit:
        return inverse(self._state_propagation)

    @cached_property
    def _state_propagation(self) -> Circuit:
        return StatePropagator(target_qubits=self.target_qubits, first_qubit_preparer=self._first_qubit_preparer).create_circuit()
