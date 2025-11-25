from cirq import Circuit, CircuitOperation, FrozenCircuit, M, Moment, TaggedOperation

from cirq_experiments.conditions import MajorityVote, MultipleConditions
from cirq_experiments.support.measurer.measurer import FAULT_TOLERANT_MEASURER_TAG, Measurer
from cirq_experiments.support.operations_applier.operations_applier_using_cat_state import \
    OperationsApplierUsingCatStateControl
from cirq_experiments.globals.fresh_ancillas_pool import FreshAncillasPool


class FaultTolerantMeasurerParallel(Measurer):
    def get_measurement_circuit(self) -> Circuit:
        if not self._measurement_keys:
            return Circuit()

        conditions = [
            MajorityVote(desired_measurement_key=measurement_key)
            for measurement_key in self._measurement_keys
        ]
        with FreshAncillasPool().parallel(use_parallel=True):
            with FreshAncillasPool().use_fresh_ancillas(num_ancillas=len(self._observables)) as ancilla_qubits:
                return Circuit(
                    TaggedOperation(
                        CircuitOperation(
                            FrozenCircuit(
                                [
                                    OperationsApplierUsingCatStateControl(operations=operations, measurement_qubit=measurement_qubit).get_application_circuit()
                                    for measurement_qubit, operations in zip(ancilla_qubits, self._observables)
                                ],
                                Moment(
                                    [
                                        M(measurement_qubit, key=condition.key)
                                        for measurement_qubit, condition in zip(ancilla_qubits, conditions)
                                    ],
                                ),
                            ),
                            use_repetition_ids=False,
                            repeat_until=MultipleConditions(conditions),
                        ),
                        FAULT_TOLERANT_MEASURER_TAG,
                    ),
                )
