from cirq import LineQubit, MeasurementKey, Simulator, Z
from numpy.ma.core import allequal, array

from stim_experiments.error_correcting_codes.support.measurer.fault_tolerant_measurer_fast_measurement import \
    FaultTolerantMeasurerFastMeasurement
from stim_experiments.globals.fresh_ancillas_pool import FreshAncillasPool
from stim_experiments.simulations.error_correcting_simulator import get_error_correcting_simulator
from stim_experiments.utilities.utilities import KET_PLUS_STATE_VECTOR
from tests.utilities_for_tests import set_seed


class TestFaultTolerantMeasurer:
    def test_no_operations(self):
        measurement_key = MeasurementKey('TEST')
        measurer = FaultTolerantMeasurerFastMeasurement(operations=[], measurement_key=measurement_key)
        circuit = measurer.get_measurement_circuit()
        initial_state = KET_PLUS_STATE_VECTOR
        utilities = get_error_correcting_simulator(state=initial_state)
        simulation = utilities.get_state_after_circuit(circuit=circuit,
                                                       num_data_qubits=1,
                                                       initial_data_state=initial_state)
        assert simulation.measurements[measurement_key.name] == array([0])

    def test_one_qubit_z(self):
        qubits = LineQubit.range(1)
        FreshAncillasPool().set_first_ancilla_num(first_ancilla_num=len(qubits))
        measurement_key = MeasurementKey('TEST')
        measurer = FaultTolerantMeasurerFastMeasurement(operations=[Z(qubits[0])], measurement_key=measurement_key)
        circuit = measurer.get_measurement_circuit()

        initial_target_state = KET_PLUS_STATE_VECTOR
        utilities = get_error_correcting_simulator(state=initial_target_state)

        num_trials = 5
        measurements = []
        for trial in range(num_trials):
            set_seed(trial)
            simulation = utilities.get_state_after_circuit(circuit=circuit,
                                                           num_data_qubits=len(qubits),
                                                           initial_data_state=initial_target_state)
            measurements.extend(simulation.measurements[measurement_key.name])
        assert any(measurements) and not all(measurements)

    def test_takes_majority_vote(self):
        qubits = LineQubit.range(1)
        FreshAncillasPool().set_first_ancilla_num(first_ancilla_num=len(qubits))
        measurement_key = MeasurementKey('TEST')
        measurer = FaultTolerantMeasurerFastMeasurement(operations=[Z(qubits[0])],
                                                        measurement_key=measurement_key)
        circuit = measurer.get_measurement_circuit()

        simulator = Simulator()
        simulation = simulator.run(circuit)
        assert len(simulation.records) == 2
        assert allequal(simulation.records[measurement_key.name], [[[0]]])
        assert allequal(next(records for key, records in simulation.records.items() if key != measurement_key.name), [[[0], [0], [0,]]])
