from uuid import uuid4

from cirq import Circuit, CircuitOperation, FrozenCircuit, OP_TREE, TaggedOperation

from stim_experiments.error_correcting_codes.error_correcting_code.error_correcting_code import ErrorCorrectingCode
from stim_experiments.error_correcting_codes.support.operations_applier.operations_applier import DELAYED_NOISE_TAG

CORRECTION_ROUND_TAG = 'CORRECTION_ROUND'
CORRECTION_ROUND_SYNDROMES_TAG = 'CORRECTION_ROUND_SYNDROMES'
CORRECTION_ROUND_RECOVERIES_TAG = 'CORRECTION_ROUND_RECOVERIES'
ENCODING_NUM_TAG = 'ENCODING_NUM'


class ActiveEncodingsStore:
    _tracked_encodings: dict[str, list[ErrorCorrectingCode]] = {}

    def __init__(self, additional_tracked_encodings: list[ErrorCorrectingCode]):
        self._id = uuid4().hex
        self._tracked_encodings[self._id] = additional_tracked_encodings

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        del self._tracked_encodings[self._id]

    def get_all_correction_circuits(self) -> OP_TREE:
        correction_circuits = [encoding.get_error_correction_circuit()  # TODO make sure syndromes use parallel ancillas
                               for encodings in self._tracked_encodings.values()
                               for encoding in encodings]
        syndrome_circuits = [correction_circuit.syndrome_circuit for correction_circuit in correction_circuits]
        recovery_circuits = [correction_circuit.recovery_circuit for correction_circuit in correction_circuits]
        return Circuit(
            TaggedOperation(
                CircuitOperation(
                    FrozenCircuit(
                        TaggedOperation(
                            CircuitOperation(
                                FrozenCircuit(
                                    TaggedOperation(
                                        CircuitOperation(syndrome_circuit.freeze()),
                                        f'{ENCODING_NUM_TAG}_{i}',
                                    )
                                    for i, syndrome_circuit in enumerate(syndrome_circuits)
                                ),
                            ),
                            CORRECTION_ROUND_SYNDROMES_TAG
                        ),
                        TaggedOperation(
                            CircuitOperation(
                                FrozenCircuit(
                                    TaggedOperation(
                                        CircuitOperation(recovery_circuit.freeze()),
                                        f'{ENCODING_NUM_TAG}_{i}',
                                    )
                                    for i, recovery_circuit in enumerate(recovery_circuits)
                                ),
                            ),
                            CORRECTION_ROUND_RECOVERIES_TAG, DELAYED_NOISE_TAG
                        )
                    )
                ),
                CORRECTION_ROUND_TAG
            )
        )
