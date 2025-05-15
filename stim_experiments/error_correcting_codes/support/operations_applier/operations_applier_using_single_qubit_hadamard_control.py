from cirq import Circuit, H

from stim_experiments.error_correcting_codes.support.operations_applier.operations_applier import OperationsApplier
from stim_experiments.singletons.fresh_ancillas_pool import FreshAncillasPool


class OperationsApplierUsingSingleQubitHadamardControl(OperationsApplier):
    def get_application_circuit(self) -> Circuit:
        # TODO move validate and no operations to base class
        self._validate()
        if not self._operations:
            return Circuit()

        with FreshAncillasPool().use_fresh_ancillas(num_ancillas=1 - bool(self._measurement_qubit)) as ancilla_qubits:
            self._measurement_qubit = self._measurement_qubit or ancilla_qubits[0]
            return Circuit(
                H(self._measurement_qubit),
                [
                    operation.controlled_by(self._measurement_qubit)
                    for operation in self._operations
                ],
            )
