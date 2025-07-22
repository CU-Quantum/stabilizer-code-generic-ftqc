from cirq import Circuit, CircuitOperation, M, R, TaggedOperation

from stim_experiments.conditions.majority_vote import \
    MajorityVote
from stim_experiments.error_correcting_codes.support.measurer.measurer import Measurer
from stim_experiments.error_correcting_codes.support.operations_applier.operations_applier_using_cat_state.operations_applier_using_cat_state import \
    OperationsApplierUsingCatStateControl
from stim_experiments.globals.fresh_ancillas_pool import FreshAncillasPool


FAULT_TOLERANT_MEASURER_FAST_MEASUREMENT_TAG = 'FAULT_TOLERANT_MEASURER'


class FaultTolerantMeasurerFastMeasurement(Measurer):
    def get_measurement_circuit(self) -> Circuit:
        with FreshAncillasPool().use_fresh_ancillas(num_ancillas=1) as ancilla_qubits:
            measurement_qubit = ancilla_qubits[0]
            applier = OperationsApplierUsingCatStateControl(operations=self._operations,
                                                            measurement_qubit=measurement_qubit,
                                                            tag=self._tag)
            condition = MajorityVote(desired_measurement_key=self._measurement_key)
            return Circuit(
                TaggedOperation(
                    CircuitOperation(
                        Circuit(
                            R(measurement_qubit),
                            applier.get_application_circuit(),
                            M(measurement_qubit, key=condition.key),
                            R(measurement_qubit),
                        ).freeze(),
                        use_repetition_ids=False,
                        repeat_until=condition
                    ),
                    FAULT_TOLERANT_MEASURER_FAST_MEASUREMENT_TAG, self._tag
                )
            )
