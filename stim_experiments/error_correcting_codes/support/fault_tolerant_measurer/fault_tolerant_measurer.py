from functools import cached_property
from typing import Callable, Optional

from cirq import Circuit, CircuitOperation, H, KeyCondition, LineQubit, M, MeasurementKey, Operation, R, X

from stim_experiments.error_correcting_codes.support.fault_tolerant_measurer.support.conditions.three_repetitions_majority_vote import \
    ThreeRepetitionsMajorityVote
from stim_experiments.error_correcting_codes.support.fault_tolerant_measurer.support.cat_state_creator_basic_undeterministic import \
    CatStateCreatorBasicUndeterministic
from stim_experiments.error_correcting_codes.support.fault_tolerant_measurer.support.controlled_single_qubit_gates_applier import \
    ControlledSingleQubitGatesApplier
from stim_experiments.utilities import FreshAncillasPool


class OperationsApplierUsingCatState:
    def __init__(self,
                 operations: list[Operation],
                 initial_control_qubit: Optional[LineQubit] = None,
                 ):
        self._operations = operations
        self._initial_control_qubit = initial_control_qubit

    def get_circuit(self) -> Circuit:
        self._validate()
        if not self._operations:
            return Circuit()

        with FreshAncillasPool().use_fresh_ancillas(num_ancillas=len(self._operations) - bool(self._initial_control_qubit)) as ancilla_qubits:
            control_qubits = [self._initial_control_qubit] + ancilla_qubits if self._initial_control_qubit else ancilla_qubits
            propagated_state = CatStateCreatorBasicUndeterministic(target_qubits=control_qubits)
            return Circuit(
                propagated_state.prepare_state(),
                ControlledSingleQubitGatesApplier(operations=self._operations, controls=control_qubits).get_circuit().freeze(),
                propagated_state.decode_state(),
            )

    def _validate(self) -> None:
        self._validate_disjoint_qubits()

    def _validate_disjoint_qubits(self) -> None:
        operation_qubits = [qubit for operation in self._operations for qubit in operation.qubits]
        if self._initial_control_qubit in operation_qubits:
            raise ValueError(f"The target qubits and measurement qubit must be disjoint. "
                             f"Found duplicate qubit {self._initial_control_qubit}.")


class FaultTolerantMeasurer:
    def __init__(self,
                 operations: list[Operation],
                 measurement_key: Optional[MeasurementKey] = None,
                 ):
        self._operations = operations
        self._measurement_key = measurement_key

    def get_measurement_circuit(self) -> Circuit:
        with FreshAncillasPool().use_fresh_ancillas(num_ancillas=1) as ancilla_qubits:
            measurement_qubit = ancilla_qubits[0]
            applier = OperationsApplierUsingCatState(operations=self._operations,
                                                     initial_control_qubit=measurement_qubit)
            condition = ThreeRepetitionsMajorityVote(desired_measurement_key=self._measurement_key)
            return Circuit(
                CircuitOperation(
                    Circuit(
                        applier.get_circuit(),
                        M(measurement_qubit, key=condition.key),
                        R(measurement_qubit),
                    ).freeze(),
                    use_repetition_ids=False,
                    repeat_until=condition
                ),
            )
