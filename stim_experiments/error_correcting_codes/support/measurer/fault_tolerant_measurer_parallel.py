from cirq import Circuit, CircuitOperation, M, ResetChannel, \
    TaggedOperation

from stim_experiments.conditions.majority_vote import \
    MajorityVote
from stim_experiments.conditions.multiple_conditions import MultipleConditions
from stim_experiments.error_correcting_codes.support.measurer.measurer import Measurer
from stim_experiments.error_correcting_codes.support.operations_applier.operations_applier_using_cat_state import \
    OperationsApplierUsingCatStateControl
from stim_experiments.globals.fresh_ancillas_pool import FreshAncillasPool


FAULT_TOLERANT_MEASURER_PARALLEL_TAG = 'FAULT_TOLERANT_MEASURER_PARALLEL'


class FaultTolerantMeasurerParallel(Measurer):
    def get_measurement_circuit(self) -> Circuit:
        if not self._measurement_keys:
            return Circuit()
        with FreshAncillasPool().use_fresh_ancillas(num_ancillas=len(self._observables)) as ancilla_qubits:
            conditions = [
                MajorityVote(desired_measurement_key=measurement_key)
                for measurement_key in self._measurement_keys
            ]
            return Circuit(
                TaggedOperation(
                    CircuitOperation(
                        Circuit(
                            ResetChannel().on_each(*ancilla_qubits),
                            [
                                OperationsApplierUsingCatStateControl(operations=operations, measurement_qubit=measurement_qubit).get_application_circuit()
                                for measurement_qubit, operations in zip(ancilla_qubits, self._observables)
                            ],
                            [
                                M(measurement_qubit, key=condition.key)
                                for measurement_qubit, condition in zip(ancilla_qubits, conditions)
                            ],
                        ).freeze(),
                        use_repetition_ids=False,
                        repeat_until=MultipleConditions(conditions)
                    ),
                    FAULT_TOLERANT_MEASURER_PARALLEL_TAG,
                ),
                ResetChannel().on_each(*ancilla_qubits),
            )
