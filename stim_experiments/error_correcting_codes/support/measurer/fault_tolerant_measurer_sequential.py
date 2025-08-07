from cirq import Circuit, CircuitOperation, ClassicalDataDictionaryStore, Condition, M, MeasurementKey, R, \
    TaggedOperation
from cirq.protocols import json_serialization

from stim_experiments.conditions.majority_vote import \
    MajorityVote
from stim_experiments.error_correcting_codes.support.measurer.measurer import FAULT_TOLERANT_MEASURER_TAG, Measurer
from stim_experiments.error_correcting_codes.support.operations_applier.operations_applier_using_cat_state import \
    OperationsApplierUsingCatStateControl
from stim_experiments.globals.fresh_ancillas_pool import FreshAncillasPool


class FaultTolerantMeasurerSequential(Measurer):
    def get_measurement_circuit(self) -> Circuit:
        with FreshAncillasPool().use_fresh_ancillas(num_ancillas=1) as ancilla_qubits:
            measurement_qubit = ancilla_qubits[0]
            appliers = [
                OperationsApplierUsingCatStateControl(operations=operations, measurement_qubit=measurement_qubit)
                for operations in self._observables
            ]
            conditions = [MajorityVote(desired_measurement_key=measurement_key) for measurement_key in self._measurement_keys]
            return Circuit(
                [
                    TaggedOperation(
                        CircuitOperation(
                            Circuit(
                                applier.get_application_circuit(),
                                M(measurement_qubit, key=condition.key),
                            ).freeze(),
                            use_repetition_ids=False,
                            repeat_until=condition
                        ),
                        FAULT_TOLERANT_MEASURER_TAG,
                    )
                    for applier, condition in zip(appliers, conditions)
                ],
            )
