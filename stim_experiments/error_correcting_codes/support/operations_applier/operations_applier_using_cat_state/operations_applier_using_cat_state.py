from cirq import Circuit, CircuitOperation, Operation, R, TaggedOperation

from stim_experiments.error_correcting_codes.support.cat_state_creator.cat_state_creator_basic_nondeterministic.cat_state_creator_basic_nondeterministic import \
    CatStateCreatorBasicNondeterministic
from stim_experiments.error_correcting_codes.support.controlled_single_qubit_gates_applier import \
    ControlledSingleQubitGatesApplier
from stim_experiments.error_correcting_codes.support.operations_applier.operations_applier import OperationsApplier
from stim_experiments.globals.fresh_ancillas_pool import FreshAncillasPool


OPERATIONS_APPLIER_USING_CAT_STATE_CONTROL_TAG = 'OPERATIONS_APPLIER_USING_CAT_STATE_CONTROL'
DELIMITER = '-'


class OperationsApplierUsingCatStateControl(OperationsApplier):
    def __init__(self, operations: list[Operation], measurement_qubit: int, tag: str):
        super().__init__(operations=operations, measurement_qubit=measurement_qubit)
        self._tag = tag

    def _perform_get_application_circuit(self) -> Circuit:
        with FreshAncillasPool().use_fresh_ancillas(num_ancillas=len(self._operations) - 1) as ancilla_qubits:
            control_qubits = [self._measurement_qubit] + ancilla_qubits
            cat_state_creator = CatStateCreatorBasicNondeterministic(qubit_register=control_qubits)
            return Circuit(
                [R(qubit) for qubit in ancilla_qubits],
                cat_state_creator.get_cat_state_circuit(),
                TaggedOperation(
                    CircuitOperation(
                        ControlledSingleQubitGatesApplier(operations=self._operations, controls=control_qubits).get_circuit().freeze(),
                    ),
                    f'{OPERATIONS_APPLIER_USING_CAT_STATE_CONTROL_TAG}{DELIMITER}{self._tag}'
                ),
                cat_state_creator.decode_state(),
                [R(qubit) for qubit in ancilla_qubits]
            )
