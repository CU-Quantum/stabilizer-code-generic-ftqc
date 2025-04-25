from typing import Optional

from cirq import Circuit, CircuitOperation, Gate, LineQubit, M, R, inverse

from stim_experiments.error_correcting_codes.support.fault_tolerant_measurer.support.conditions.three_repetitions_majority_vote import \
    ThreeRepetitionsMajorityVote
from stim_experiments.error_correcting_codes.support.fault_tolerant_measurer.support.cat_state_circuit_creator import \
    CatStateCircuitCreator
from stim_experiments.error_correcting_codes.support.fault_tolerant_measurer.support.control_qubits_preparer import \
    ControlQubitsPreparer
from stim_experiments.error_correcting_codes.support.fault_tolerant_measurer.support.controlled_single_qubit_gates_applier import \
    ControlledSingleQubitGatesApplier


class FaultTolerantMeasurer:
    def __init__(self,
                 gates: list[Gate],
                 targets: list[LineQubit],
                 measurement_qubit: LineQubit,
                 ancillas: list[LineQubit],
                 measurement_key: Optional[str] = None,
                 ):
        self._gates = gates
        self._targets = targets
        self._measurement_qubit = measurement_qubit
        self._ancillas = ancillas
        self._measurement_key = measurement_key

    def get_measurement_circuit(self) -> Circuit:
        self._validate()
        condition = ThreeRepetitionsMajorityVote(desired_measurement_key=self._measurement_key)
        circuit = Circuit(
            ControlQubitsPreparer(target_qubits=self._control, verifier_ancilla=self._verifier_ancilla).prepare_state(),
            ControlledSingleQubitGatesApplier(gates=self._gates, targets=self._targets, controls=self._control).get_circuit(),
            inverse(CatStateCircuitCreator(target_qubits=self._control).create_circuit()),
            M(self._measurement_qubit, key=condition.key),
            R(self._measurement_qubit),
        )
        return Circuit(CircuitOperation(circuit.freeze(), use_repetition_ids=False, repeat_until=condition))

    def _validate(self) -> None:
        self._validate_num_ancillas()
        self._validate_disjoint_qubits()

    def _validate_num_ancillas(self) -> None:
        if len(self._ancillas) < len(self._gates):
            raise ValueError(
                f"The number of ancillas ({len(self._ancillas)}) must be at least the number of gates ({len(self._gates)}).")

    def _validate_disjoint_qubits(self) -> None:
        qubits = self._targets + [self._measurement_qubit] + self._ancillas
        qubits_set = set(qubits)
        if len(qubits) != len(qubits_set):
            duplicates = qubits.copy()
            for qubit in qubits_set:
                duplicates.remove(qubit)
            raise ValueError(f"The target qubits, measurement qubit, and ancilla qubits must be disjoint. "
                             f"Found duplicate qubit(s) {set(duplicates)}.")

    @property
    def _control(self) -> list[LineQubit]:
        return [self._measurement_qubit] + self._ancillas[:len(self._gates) - 1]

    @property
    def _verifier_ancilla(self) -> LineQubit:
        return self._ancillas[-1]
