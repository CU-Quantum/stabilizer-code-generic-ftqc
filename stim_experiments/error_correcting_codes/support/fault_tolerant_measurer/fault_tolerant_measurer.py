from functools import cached_property
from typing import Callable, Optional

from cirq import Circuit, CircuitOperation, H, KeyCondition, LineQubit, M, MeasurementKey, Operation, R, X

from stim_experiments.error_correcting_codes.support.fault_tolerant_measurer.support.conditions.three_repetitions_majority_vote import \
    ThreeRepetitionsMajorityVote
from stim_experiments.error_correcting_codes.support.fault_tolerant_measurer.support.control_qubits_preparer import \
    StatePropagationParityEnsurer
from stim_experiments.error_correcting_codes.support.fault_tolerant_measurer.support.controlled_single_qubit_gates_applier import \
    ControlledSingleQubitGatesApplier


class FaultTolerantApplier:
    def __init__(self,
                 operations: list[Operation],
                 measurement_qubit: LineQubit,
                 ancillas: list[LineQubit],
                 measurement_qubit_preparer: Circuit,
                 ):
        self._operations = operations
        self._measurement_qubit = measurement_qubit
        self._ancillas = ancillas
        self._measurement_qubit_preparer = measurement_qubit_preparer

    def get_circuit(self) -> Circuit:
        self._validate()
        if not self._operations:
            return Circuit()

        control_qubits = [self._measurement_qubit] + self._ancillas[:len(self._operations) - 1]
        propagated_state = StatePropagationParityEnsurer(target_qubits=control_qubits,
                                                         verifier_ancilla=self.verifier_ancilla,
                                                         first_qubit_preparer=self._measurement_qubit_preparer,
                                                         )
        return Circuit(
            propagated_state.prepare_state(),
            ControlledSingleQubitGatesApplier(operations=self._operations, controls=control_qubits).get_circuit(),
            propagated_state.decode_state(),
        )

    def _validate(self) -> None:
        self._validate_num_ancillas()
        self._validate_disjoint_qubits()

    def _validate_num_ancillas(self) -> None:
        if len(self._ancillas) < len(self._operations) - 1:
            raise ValueError(
                f"The number of ancillas ({len(self._ancillas)}) must be at least the one less than number of operations ({len(self._operations) - 1}).")

    def _validate_disjoint_qubits(self) -> None:
        operation_qubits = [qubit for operation in self._operations for qubit in operation.qubits]  # TODO test allows multiple operations on same qubit
        duplicates = {ancilla for ancilla in self._ancillas if ancilla in operation_qubits}
        if self._measurement_qubit in operation_qubits or self._measurement_qubit in self._ancillas:
            duplicates.add(self._measurement_qubit)
        if duplicates:
            raise ValueError(f"The target qubits, measurement qubit, and ancilla qubits must be disjoint. "
                             f"Found duplicate qubit(s) {set(duplicates)}.")

    @cached_property
    def verifier_ancilla(self) -> Optional[LineQubit]:
        return self._ancillas[-1] if len(self._ancillas) else None


class FaultTolerantMeasurer:
    def __init__(self,
                 operations: list[Operation],
                 measurement_qubit: LineQubit,
                 ancillas: list[LineQubit],
                 measurement_key: Optional[str] = None,
                 ):
        self._operations = operations
        self._measurement_qubit = measurement_qubit
        self._ancillas = ancillas
        self._measurement_key = measurement_key or MeasurementKey(repr(self._measurement_qubit))

    def get_measurement_circuit(self) -> Circuit:
        hadamard_first_qubit = Circuit(H(self._measurement_qubit))
        applier = FaultTolerantApplier(operations=self._operations,
                                       measurement_qubit=self._measurement_qubit,
                                       ancillas=self._ancillas,
                                       measurement_qubit_preparer=hadamard_first_qubit,
                                       )
        condition = ThreeRepetitionsMajorityVote(desired_measurement_key=self._measurement_key)
        return Circuit(
            CircuitOperation(
                Circuit(
                    applier.get_circuit(),
                    M(self._measurement_qubit, key=condition.key),
                    R(self._measurement_qubit),
                ).freeze(),
                use_repetition_ids=False,
                repeat_until=condition
            ),
        )
