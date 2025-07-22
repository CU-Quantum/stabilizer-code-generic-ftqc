from cirq import Circuit, I, LineQubit, MeasurementKey
from numpy import array, sqrt

from stim_experiments.custom_dataclasses.state_and_measurements import \
    StateAndMeasurements
from stim_experiments.error_correcting_codes.support.measurer.fault_tolerant_measurer_fast_measurement.support.parity_verifier import \
    ParityVerifier
from stim_experiments.globals.fresh_ancillas_pool import FreshAncillasPool
from stim_experiments.simulations.error_correcting_simulator import get_error_correcting_simulator
from stim_experiments.utilities.utilities import KET_ONE_STATE_VECTOR, KET_ZERO_STATE_VECTOR, tensor
from tests.utilities import get_cat_state_vector


class TestParityVerifier:
    def test_trivial(self):
        verifier = ParityVerifier(target_qubits=[], measurement_key=MeasurementKey('arbitrary'))
        circuit = verifier.validate_parity()
        assert circuit == Circuit()

    def test_valid_cat_state_one_qubit(self):
        qubits = LineQubit.range(1)
        verifier = ParityVerifier(target_qubits=qubits, measurement_key=MeasurementKey('arbitrary'))
        circuit = Circuit(
            I(qubits[0]),
            verifier.validate_parity()
        )

        one_qubit_cat_state = get_cat_state_vector(num_qubits=1)
        error_correcting_code_utilities = get_error_correcting_simulator(state=one_qubit_cat_state)
        state = error_correcting_code_utilities.get_state_after_circuit(circuit=circuit,
                                                                        num_data_qubits=len(qubits),
                                                                        initial_data_state=one_qubit_cat_state)
        assert state == StateAndMeasurements(
            state=one_qubit_cat_state,
            measurements={}
        )

    def test_valid_cat_state_two_qubit(self):
        qubits = LineQubit.range(2)
        FreshAncillasPool().set_first_ancilla_num(len(qubits))
        measurement_key = MeasurementKey('arbitrary')
        verifier = ParityVerifier(target_qubits=qubits, measurement_key=MeasurementKey('arbitrary'))
        circuit = Circuit(
            [I(qubit) for qubit in qubits],
            verifier.validate_parity()
        )

        two_qubit_cat_state = get_cat_state_vector(num_qubits=len(qubits))
        error_correcting_code_utilities = get_error_correcting_simulator(state=two_qubit_cat_state)
        state = error_correcting_code_utilities.get_state_after_circuit(circuit=circuit,
                                                                        num_data_qubits=len(qubits),
                                                                        initial_data_state=two_qubit_cat_state)
        assert state == StateAndMeasurements(
            state=two_qubit_cat_state,
            measurements={measurement_key.name: array([0])}
        )

    def test_invalid_cat_state_two_qubit(self):
        qubits = LineQubit.range(2)
        FreshAncillasPool().set_first_ancilla_num(len(qubits))
        measurement_key = MeasurementKey('arbitrary')
        verifier = ParityVerifier(target_qubits=qubits, measurement_key=measurement_key)
        circuit = verifier.validate_parity()

        invalid_cat_state = tensor(KET_ZERO_STATE_VECTOR, KET_ONE_STATE_VECTOR)
        error_correcting_code_utilities = get_error_correcting_simulator(state=invalid_cat_state)
        state = error_correcting_code_utilities.get_state_after_circuit(circuit=circuit,
                                                                        num_data_qubits=len(qubits),
                                                                        initial_data_state=invalid_cat_state)
        assert state == StateAndMeasurements(
            state=invalid_cat_state,
            measurements={measurement_key.name: array([1])}
        )

    def test_valid_cat_state_three_qubit(self):
        qubits = LineQubit.range(3)
        FreshAncillasPool().set_first_ancilla_num(len(qubits))
        measurement_key = MeasurementKey('arbitrary')
        verifier = ParityVerifier(target_qubits=qubits, measurement_key=measurement_key)
        circuit = verifier.validate_parity()

        three_qubit_cat_state = get_cat_state_vector(num_qubits=3)
        error_correcting_code_utilities = get_error_correcting_simulator(state=three_qubit_cat_state)
        state = error_correcting_code_utilities.get_state_after_circuit(circuit=circuit,
                                                                        num_data_qubits=len(qubits),
                                                                        initial_data_state=three_qubit_cat_state)
        assert state == StateAndMeasurements(
            state=three_qubit_cat_state,
            measurements={measurement_key.name: array([0])}
        )

    def test_invalid_cat_state_three_qubit(self):
        qubits = LineQubit.range(3)
        FreshAncillasPool().set_first_ancilla_num(len(qubits))
        measurement_key = MeasurementKey('arbitrary')
        verifier = ParityVerifier(target_qubits=qubits, measurement_key=measurement_key)
        circuit = verifier.validate_parity()

        invalid_three_qubit_cat_state = (
                    (1 / sqrt(2)) * (tensor(KET_ZERO_STATE_VECTOR, KET_ZERO_STATE_VECTOR, KET_ONE_STATE_VECTOR)
                                     + tensor(KET_ONE_STATE_VECTOR, KET_ONE_STATE_VECTOR, KET_ZERO_STATE_VECTOR)))
        error_correcting_code_utilities = get_error_correcting_simulator(state=invalid_three_qubit_cat_state)
        state = error_correcting_code_utilities.get_state_after_circuit(circuit=circuit,
                                                                        num_data_qubits=len(qubits),
                                                                        initial_data_state=invalid_three_qubit_cat_state)
        assert state == StateAndMeasurements(
            state=invalid_three_qubit_cat_state,
            measurements={measurement_key.name: array([1])}
        )
