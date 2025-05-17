from functools import cached_property
from uuid import uuid4

from cirq import Circuit, CircuitOperation, LineQubit, MeasurementKey, R, inverse

from stim_experiments.error_correcting_codes.support.cat_state_creator.cat_state_creator import CatStateCreator
from stim_experiments.conditions.verification_is_zero import \
    VerificationIsZero
from stim_experiments.error_correcting_codes.support.measurer.fault_tolerant_measurer.support.parity_verifier import \
    ParityVerifier
from stim_experiments.error_correcting_codes.support.cat_state_creator.cat_state_creator_cx_from_first_qubit import \
    CatStateCreatorCxFromFirstQubit


class CatStateCreatorBasicNondeterministic(CatStateCreator):
    # TODO test class
    def __init__(self, qubit_register: list[LineQubit]):
        super().__init__(qubit_register=qubit_register)

    def get_cat_state_circuit(self) -> Circuit:
        verification_condition = VerificationIsZero(key=MeasurementKey(f'VERIFICATION_{uuid4().hex}'))
        preparation_circuit = Circuit(
            [R(qubit) for qubit in self._qubit_register.copy()],
            self._state_propagation,
            ParityVerifier(target_qubits=self._qubit_register, measurement_key=verification_condition.key).validate_parity(),
        )
        return Circuit(
            CircuitOperation(preparation_circuit.freeze(),
                             use_repetition_ids=False,
                             repeat_until=verification_condition if len(self._qubit_register) > 1 else None),
        )

    def decode_state(self) -> Circuit:
        return inverse(self._state_propagation)

    @cached_property
    def _state_propagation(self) -> Circuit:
        return CatStateCreatorCxFromFirstQubit(qubit_register=self._qubit_register).get_cat_state_circuit()
