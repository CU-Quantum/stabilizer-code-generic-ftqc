from cirq import LineQubit, MeasurementKey, Simulator, Z
from numpy.ma.core import allequal

from cirq_experiments.support.measurer.fault_tolerant_measurer_sequential import \
    FaultTolerantMeasurerSequential
from cirq_experiments.globals.fresh_ancillas_pool import FreshAncillasPool
from cirq_experiments.simulations.error_correcting_simulator import get_error_correcting_simulator
from cirq_experiments.utilities.utilities import KET_PLUS_STATE_VECTOR
from tests.cirq_experiments.utilities_for_tests import set_seed


class TestFaultTolerantMeasurerSequential:
    def test_one_qubit_z(self):
        qubits = LineQubit.range(1)
        FreshAncillasPool().set_first_ancilla_num(first_ancilla_num=len(qubits))
        measurement_key = MeasurementKey('TEST')
        measurer = FaultTolerantMeasurerSequential(observables=[[Z(qubits[0])]], measurement_keys=[measurement_key])
        circuit = measurer.get_measurement_circuit()

        initial_target_state = KET_PLUS_STATE_VECTOR
        utilities = get_error_correcting_simulator(state=initial_target_state)

        num_trials = 5
        measurements = []
        for trial in range(num_trials):
            set_seed(trial)
            simulation = utilities.run_simulation(circuit=circuit,
                                                  num_data_qubits=len(qubits),
                                                  initial_data_state=initial_target_state)
            measurements.extend(simulation.measurements[measurement_key.name])
        assert any(measurements) and not all(measurements)

    def test_takes_majority_vote(self):
        qubits = LineQubit.range(1)
        FreshAncillasPool().set_first_ancilla_num(first_ancilla_num=len(qubits))
        measurement_key = MeasurementKey('TEST')
        measurer = FaultTolerantMeasurerSequential(observables=[[Z(qubits[0])]],
                                                   measurement_keys=[measurement_key])
        circuit = measurer.get_measurement_circuit()

        simulator = Simulator()
        simulation = simulator.run(circuit)
        assert len(simulation.records) == 2
        assert allequal(simulation.records[measurement_key.name], [[[0]]])
        assert allequal(next(records for key, records in simulation.records.items() if key != measurement_key.name), [[[0], [0], [0,]]])
