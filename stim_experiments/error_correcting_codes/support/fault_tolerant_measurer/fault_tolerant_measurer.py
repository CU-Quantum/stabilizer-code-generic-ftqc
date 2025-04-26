from functools import cached_property
from typing import Callable, Optional

from cirq import Circuit, CircuitOperation, H, KeyCondition, LineQubit, MeasurementKey, Operation, R, X

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
                 measurement_key: Optional[str] = None,
                 ):
        self._operations = operations
        self._measurement_qubit = measurement_qubit
        self._ancillas = ancillas
        self._measurement_qubit_preparer = measurement_qubit_preparer
        self._measurement_key = measurement_key or MeasurementKey(repr(self._measurement_qubit))

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

    # measurement_qubits = [self._measurement_qubit] + LineQubit.range(self._total_num_qubits, self._total_num_qubits + 2)
    # voters = [
    #     StatePropagationParityEnsurer(target_qubits=[measurement_qubit] + self._ancillas[:len(self._operations) - 1],
    #                                   verifier_ancilla=self.verifier_ancilla,
    #                                   first_qubit_preparer=self._measurement_qubit_preparer(measurement_qubit),
    #                                   )
    #     for measurement_qubit in measurement_qubits
    # ]
    # votes = [
    #     [
    #         voter.prepare_state(),
    #         ControlledSingleQubitGatesApplier(operations=self._operations, controls=voter.target_qubits).get_circuit(),
    #         voter.decode_state()
    #     ]
    #     for voter in voters
    # ]
    # circuit = Circuit(
    #     votes,
    #     X(LineQubit(measurement_qubits[-1].x + 1)).controlled_by(measurement_qubits[0]),
    #     X(LineQubit(measurement_qubits[-1].x + 1)).controlled_by(measurement_qubits[1]),
    #     M(LineQubit(measurement_qubits[-1].x + 1), key='a'),
    #     CircuitOperation(
    #         FrozenCircuit(
    #             X(LineQubit(measurement_qubits[-1].x + 2)).controlled_by(measurement_qubits[1]),
    #             X(LineQubit(measurement_qubits[-1].x + 2)).controlled_by(measurement_qubits[2]),
    #             M(LineQubit(measurement_qubits[-1].x + 2), key='b'),
    #         ),
    #         repeat_until=
    #     )
    #
    #
    #
    # )

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
                                       measurement_key=self._measurement_key,
                                       )
        condition = ThreeRepetitionsMajorityVote(desired_measurement_key=self._measurement_key)
        circuit = Circuit(
            CircuitOperation(applier.get_circuit().freeze(), use_repetition_ids=False, repeat_until=condition),
            R(self._measurement_qubit),
            X(self._measurement_qubit).with_classical_controls(KeyCondition(key=self._measurement_key))
        )
        return Circuit(
            circuit,
            R(self._measurement_qubit),
        )
