from cirq import Circuit, CircuitOperation

from stim_experiments.error_correcting_codes.support.cat_state_creator.cat_state_creator_basic_nondeterministic import \
    CatStateCreatorBasicNondeterministic
from stim_experiments.error_correcting_codes.support.operations_applier.operations_applier_using_cat_state.support.controlled_single_qubit_gates_applier import \
    ControlledSingleQubitGatesApplier
from stim_experiments.error_correcting_codes.support.operations_applier.operations_applier import OperationsApplier
from stim_experiments.utilities import FreshAncillasPool


class OperationsApplierUsingCatStateControl(OperationsApplier):
    def get_application_circuit(self) -> Circuit:
        self._validate()
        if not self._operations:
            return Circuit()

        with FreshAncillasPool().use_fresh_ancillas(num_ancillas=len(self._operations) - 1) as ancilla_qubits:
            control_qubits = [self._measurement_qubit] + ancilla_qubits
            cat_state_creator = CatStateCreatorBasicNondeterministic(qubit_register=control_qubits)
            circuit = ControlledSingleQubitGatesApplier(operations=self._operations, controls=control_qubits).get_circuit()
            return Circuit(
                cat_state_creator.get_cat_state_circuit(),
                CircuitOperation(circuit.freeze()).with_classical_controls(self._condition)
                    if self._condition
                    else circuit,
                cat_state_creator.decode_state(),
            )
