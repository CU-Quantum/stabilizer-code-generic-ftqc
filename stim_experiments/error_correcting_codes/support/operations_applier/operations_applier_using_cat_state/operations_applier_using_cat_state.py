from typing import Optional

from cirq import Circuit, CircuitOperation, Condition, LineQubit, Operation
from sympy import Expr

from stim_experiments.error_correcting_codes.support.cat_state_creator.cat_state_creator_basic_undeterministic import \
    CatStateCreatorBasicUndeterministic
from stim_experiments.error_correcting_codes.support.operations_applier.operations_applier_using_cat_state.support.controlled_single_qubit_gates_applier import \
    ControlledSingleQubitGatesApplier
from stim_experiments.error_correcting_codes.support.operations_applier.operations_applier import OperationsApplier
from stim_experiments.utilities import FreshAncillasPool


class OperationsApplierUsingCatState(OperationsApplier):
    def __init__(self,
                 operations: list[Operation],
                 initial_control_qubit: Optional[LineQubit] = None,
                 condition: Optional[Condition | Expr] = None,
                 ):
        super().__init__(operations=operations, condition=condition)
        self._initial_control_qubit = initial_control_qubit

    def get_application_circuit(self) -> Circuit:
        self._validate()
        if not self._operations:
            return Circuit()

        with FreshAncillasPool().use_fresh_ancillas(num_ancillas=len(self._operations) - bool(self._initial_control_qubit)) as ancilla_qubits:
            control_qubits = [self._initial_control_qubit] + ancilla_qubits if self._initial_control_qubit else ancilla_qubits
            propagated_state = CatStateCreatorBasicUndeterministic(qubit_register=control_qubits)
            return Circuit(
                propagated_state.get_cat_state_circuit(),
                CircuitOperation(
                    ControlledSingleQubitGatesApplier(operations=self._operations, controls=control_qubits).get_circuit().freeze()
                ).with_classical_controls(self._condition)
                    if self._condition
                    else ControlledSingleQubitGatesApplier(operations=self._operations, controls=control_qubits).get_circuit(),
                propagated_state.decode_state(),
            )

    def _validate(self) -> None:
        self._validate_disjoint_qubits()

    def _validate_disjoint_qubits(self) -> None:
        operation_qubits = [qubit for operation in self._operations for qubit in operation.qubits]
        if self._initial_control_qubit in operation_qubits:
            raise ValueError(f"The target qubits and measurement qubit must be disjoint. "
                             f"Found duplicate qubit {self._initial_control_qubit}.")
