from cirq import Circuit, LineQubit
from numpy import array, sqrt

from stim_experiments.error_correcting_codes.error_correcting_code_utilities import \
    get_error_correcting_code_utilities
from stim_experiments.error_correcting_codes.generic_stabilizer_code.custom_dataclasses.state_and_measurements import \
    StateAndMeasurements
from stim_experiments.error_correcting_codes.support.fault_tolerant_measurer.support.conditions.verification_is_zero import \
    VerificationIsZero
from stim_experiments.error_correcting_codes.support.fault_tolerant_measurer.support.parity_verifier import \
    ParityVerifier
from stim_experiments.utilities import KET_ONE_STATE_VECTOR, KET_ZERO_STATE_VECTOR, tensor
from tests.utilities import get_cat_state_vector


class TestParityVerifier:
    def test_trivial(self):
        verifier = ParityVerifier(target_qubits=[], verifier_ancilla=LineQubit(0))
        circuit = verifier.validate_parity()
        assert circuit == Circuit()

    def test_valid_cat_state_one_qubit(self):
        qubits = LineQubit.range(1)
        verifier = ParityVerifier(target_qubits=qubits, verifier_ancilla=qubits[0])
        circuit = verifier.validate_parity()

        one_qubit_cat_state = get_cat_state_vector(num_qubits=1)
        error_correcting_code_utilities = get_error_correcting_code_utilities(state=one_qubit_cat_state)
        state = error_correcting_code_utilities.get_state_after_circuit(circuit=circuit,
                                                                        initial_state=one_qubit_cat_state,
                                                                        qubit_order=qubits,)
        assert state == StateAndMeasurements(
            state=one_qubit_cat_state,
            measurements={}
        )

    def test_valid_cat_state_two_qubit(self):
        qubits = LineQubit.range(3)
        verifier = ParityVerifier(target_qubits=qubits[:-1], verifier_ancilla=qubits[-1])
        circuit = verifier.validate_parity()

        two_qubit_cat_state = get_cat_state_vector(num_qubits=2)
        ancilla_state = KET_ZERO_STATE_VECTOR
        initial_state = tensor(two_qubit_cat_state, ancilla_state)
        error_correcting_code_utilities = get_error_correcting_code_utilities(state=initial_state)
        state = error_correcting_code_utilities.get_state_after_circuit(circuit=circuit,
                                                                        initial_state=initial_state,
                                                                        qubit_order=qubits,)
        assert state == StateAndMeasurements(
            state=initial_state,
            measurements={str(VerificationIsZero().key): array([0])}
        )

    def test_invalid_cat_state_two_qubit(self):
        qubits = LineQubit.range(3)
        verifier = ParityVerifier(target_qubits=qubits[:-1], verifier_ancilla=qubits[-1])
        circuit = verifier.validate_parity()

        invalid_cat_state = tensor(KET_ZERO_STATE_VECTOR, KET_ONE_STATE_VECTOR)
        ancilla_state = KET_ZERO_STATE_VECTOR
        initial_state = tensor(invalid_cat_state, ancilla_state)
        error_correcting_code_utilities = get_error_correcting_code_utilities(state=initial_state)
        state = error_correcting_code_utilities.get_state_after_circuit(circuit=circuit,
                                                                        initial_state=initial_state,
                                                                        qubit_order=qubits,)
        assert state == StateAndMeasurements(
            state=initial_state,
            measurements={str(VerificationIsZero().key): array([1])}
        )

    def test_valid_cat_state_three_qubit(self):
        qubits = LineQubit.range(4)
        verifier = ParityVerifier(target_qubits=qubits[:-1], verifier_ancilla=qubits[-1])
        circuit = verifier.validate_parity()

        three_qubit_cat_state = get_cat_state_vector(num_qubits=3)
        ancilla_state = KET_ZERO_STATE_VECTOR
        initial_state = tensor(three_qubit_cat_state, ancilla_state)
        error_correcting_code_utilities = get_error_correcting_code_utilities(state=initial_state)
        state = error_correcting_code_utilities.get_state_after_circuit(circuit=circuit,
                                                                        initial_state=initial_state,
                                                                        qubit_order=qubits)
        assert state == StateAndMeasurements(
            state=initial_state,
            measurements={str(VerificationIsZero().key): array([0])}
        )

    def test_invalid_cat_state_three_qubit(self):
        qubits = LineQubit.range(4)
        verifier = ParityVerifier(target_qubits=qubits[:-1], verifier_ancilla=qubits[-1])
        circuit = verifier.validate_parity()

        invalid_three_qubit_cat_state = (
                    (1 / sqrt(2)) * (tensor(KET_ZERO_STATE_VECTOR, KET_ZERO_STATE_VECTOR, KET_ONE_STATE_VECTOR)
                                     + tensor(KET_ONE_STATE_VECTOR, KET_ONE_STATE_VECTOR, KET_ZERO_STATE_VECTOR)))
        ancilla_state = KET_ZERO_STATE_VECTOR
        initial_state = tensor(invalid_three_qubit_cat_state, ancilla_state)
        error_correcting_code_utilities = get_error_correcting_code_utilities(state=initial_state)
        state = error_correcting_code_utilities.get_state_after_circuit(circuit=circuit,
                                                                        initial_state=initial_state,
                                                                        qubit_order=qubits)
        assert state == StateAndMeasurements(
            state=initial_state,
            measurements={str(VerificationIsZero().key): array([1])}
        )
