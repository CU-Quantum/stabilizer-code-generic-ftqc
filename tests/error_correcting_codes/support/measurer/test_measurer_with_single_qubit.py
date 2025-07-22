from cirq import Circuit, LineQubit, MeasurementKey, X, Z

from stim_experiments.error_correcting_codes.support.measurer.measurer_with_single_qubit import MeasurerWithSingleQubit
from stim_experiments.globals.fresh_ancillas_pool import FreshAncillasPool
from stim_experiments.simulations.error_correcting_simulator import get_error_correcting_simulator
from stim_experiments.utilities.utilities import KET_MINUS_STATE_VECTOR, KET_ONE_STATE_VECTOR, KET_PLUS_STATE_VECTOR, \
    tensor
from tests.utilities import set_seed


class TestMeasurerWithSingleQubit:
    def test_trivial(self):
        measurer = MeasurerWithSingleQubit(operations=[])
        circuit = measurer.get_measurement_circuit()
        assert circuit == Circuit()

    def test_one_operation_z(self):
        qubits = LineQubit.range(1)
        FreshAncillasPool.set_first_ancilla_num(first_ancilla_num=len(qubits))
        measurement_key = MeasurementKey('TEST')
        measurer = MeasurerWithSingleQubit(operations=[Z(qubits[0])],
                                           measurement_key=measurement_key)
        circuit = measurer.get_measurement_circuit()

        initial_state = KET_PLUS_STATE_VECTOR
        utilities = get_error_correcting_simulator(state=initial_state)

        num_trials = 5
        measurements = []
        for trial in range(num_trials):
            set_seed(trial)
            simulation = utilities.get_state_after_circuit(circuit=circuit,
                                                           num_data_qubits=len(qubits),
                                                           initial_data_state=initial_state)
            measurements.extend(simulation.measurements[measurement_key.name])
        assert any(measurements) and not all(measurements)

    def test_multiple_operations_z(self):
        qubits = LineQubit.range(2)
        FreshAncillasPool.set_first_ancilla_num(first_ancilla_num=len(qubits))
        measurement_key = MeasurementKey('TEST')
        measurer = MeasurerWithSingleQubit(operations=[X(qubits[0]), Z(qubits[1])],
                                           measurement_key=measurement_key)
        circuit = measurer.get_measurement_circuit()

        initial_state = tensor(KET_MINUS_STATE_VECTOR, KET_ONE_STATE_VECTOR)
        utilities = get_error_correcting_simulator(state=initial_state)

        num_trials = 5
        measurements = []
        for trial in range(num_trials):
            set_seed(trial)
            simulation = utilities.get_state_after_circuit(circuit=circuit,
                                                           num_data_qubits=len(qubits),
                                                           initial_data_state=initial_state)
            measurements.extend(simulation.measurements[measurement_key.name])
        assert not any(measurements)
