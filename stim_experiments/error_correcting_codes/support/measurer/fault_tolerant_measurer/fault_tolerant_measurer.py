from typing import Optional

from cirq import Circuit, CircuitOperation, M, MeasurementKey, Operation, R

from stim_experiments.error_correcting_codes.support.measurer.fault_tolerant_measurer.support.conditions.three_repetitions_majority_vote import \
    ThreeRepetitionsMajorityVote
from stim_experiments.error_correcting_codes.support.measurer.measurer import Measurer
from stim_experiments.error_correcting_codes.support.operations_applier.operations_applier_using_cat_state.operations_applier_using_cat_state import \
    OperationsApplierUsingCatStateControl
from stim_experiments.globals.fresh_ancillas_pool import FreshAncillasPool


class FaultTolerantMeasurer(Measurer):
    def __init__(self,
                 operations: list[Operation],
                 measurement_key: Optional[MeasurementKey] = None,
                 ):
        super().__init__(operations=operations, measurement_key=measurement_key)

    def get_measurement_circuit(self) -> Circuit:
        with FreshAncillasPool().use_fresh_ancillas(num_ancillas=1) as ancilla_qubits:
            measurement_qubit = ancilla_qubits[0]
            applier = OperationsApplierUsingCatStateControl(operations=self._operations,
                                                            measurement_qubit=measurement_qubit)
            condition = ThreeRepetitionsMajorityVote(desired_measurement_key=self._measurement_key)
            return Circuit(
                CircuitOperation(
                    Circuit(
                        applier.get_application_circuit(),
                        M(measurement_qubit, key=condition.key),
                        R(measurement_qubit),
                    ).freeze(),
                    use_repetition_ids=False,
                    repeat_until=condition
                ),
            )
