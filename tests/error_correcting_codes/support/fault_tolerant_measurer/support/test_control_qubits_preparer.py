from dataclasses import dataclass
from mimetypes import inited

import cirq
from cirq import Circuit, CircuitOperation, ClassicalDataStoreReader, Condition, FrozenCircuit, Gate, KeyCondition, \
    LineQubit, MeasurementKey, R, X, Z
from cirq.protocols import json_serialization
from numpy import sqrt

from stim_experiments.error_correcting_codes.error_correcting_code_utilities import get_error_correcting_code_utilities
from stim_experiments.utilities import KET_ONE_STATE_VECTOR, KET_PLUS_STATE_VECTOR, KET_ZERO_STATE_VECTOR, tensor
from tests.error_correcting_codes.support.fault_tolerant_measurer.support.test_cat_state_circuit_creator import \
    CatStateCircuitCreator
from tests.error_correcting_codes.support.fault_tolerant_measurer.support.test_parity_verifier import ParityVerifier, \
    VerificationIsZero
from tests.utilities import get_cat_state_vector, states_are_equal


class ControlQubitsPreparer:
    def __init__(self, target_qubits: list[LineQubit], verifier_ancilla: LineQubit):
        self._target_qubits = target_qubits
        self._verifier_ancilla = verifier_ancilla

    def prepare_state(self) -> Circuit:
        preparation_circuit = FrozenCircuit(Circuit(
            [R(qubit) for qubit in self._target_qubits + [self._verifier_ancilla]],
            CatStateCircuitCreator(target_qubits=self._target_qubits).create_circuit(),
            ParityVerifier(target_qubits=self._target_qubits, ancilla_qubit=self._verifier_ancilla).is_valid_cat_state(),
        ))
        return Circuit(
            CircuitOperation(preparation_circuit, use_repetition_ids=False, repeat_until=VerificationIsZero()),
        )


class TestControlQubitsPreparer:
    def test_creates_cat_state(self):
        num_target_qubits = 3
        num_ancilla_qubits = 1
        num_qubits = num_target_qubits + num_ancilla_qubits
        qubits = LineQubit.range(num_qubits)

        preparer = ControlQubitsPreparer(target_qubits=qubits[:-1], verifier_ancilla=qubits[-1])
        circuit = preparer.prepare_state()

        initial_state = tensor(*[KET_ZERO_STATE_VECTOR] * num_qubits)
        error_correction_utilities = get_error_correcting_code_utilities(state=initial_state)
        state = error_correction_utilities.get_state_after_circuit(circuit=circuit,
                                                                   qubit_order=qubits,
                                                                   initial_state=initial_state)

        expected_target_qubits_state = get_cat_state_vector(num_qubits=num_target_qubits)
        expected_ancilla_qubits_state = tensor(*[KET_ZERO_STATE_VECTOR] * num_ancilla_qubits)
        assert states_are_equal(state.state, tensor(expected_target_qubits_state, expected_ancilla_qubits_state))

    def test_retries_if_invalid(self):
        num_target_qubits = 3
        num_ancilla_qubits = 1
        num_qubits = num_target_qubits + num_ancilla_qubits
        qubits = LineQubit.range(num_qubits)

        preparer = ControlQubitsPreparer(target_qubits=qubits[:-1], verifier_ancilla=qubits[-1])
        preparer.add_error_beforehand(gate=X, qubit=qubits[1])
        circuit = preparer.prepare_state()

        initial_state = tensor(*[KET_ZERO_STATE_VECTOR] * num_qubits)
        error_correction_utilities = get_error_correcting_code_utilities(state=initial_state)
        state = error_correction_utilities.get_state_after_circuit(circuit=circuit,
                                                                   qubit_order=qubits,
                                                                   initial_state=initial_state)

        expected_target_qubits_state = get_cat_state_vector(num_qubits=num_target_qubits)
        expected_ancilla_qubits_state = tensor(*[KET_ZERO_STATE_VECTOR] * num_ancilla_qubits)
        assert states_are_equal(state.state, tensor(expected_target_qubits_state, expected_ancilla_qubits_state))

