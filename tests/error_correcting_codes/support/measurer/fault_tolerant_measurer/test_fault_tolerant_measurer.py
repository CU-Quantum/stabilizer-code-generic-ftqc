import numpy.random
import pytest
from cirq import Circuit, LineQubit, Simulator, X, \
    Z
from numpy.ma.core import allequal

from stim_experiments.error_correcting_codes.support.measurer.fault_tolerant_measurer.fault_tolerant_measurer import \
    FaultTolerantMeasurer
from stim_experiments.utilities import KET_PLUS_STATE_VECTOR, KET_ZERO_STATE_VECTOR, tensor


class TestFaultTolerantMeasurer:
    def test_trivial(self):
        measurer = FaultTolerantMeasurer(gates=[], targets=[], measurement_qubit=LineQubit(0), ancillas=[])
        circuit = measurer.get_measurement_circuit()
        assert circuit == Circuit()

    def test_one_qubit_z(self):
        numpy.random.seed(0)

        qubits = LineQubit.range(3)
        targets = qubits[:1]
        measurement_qubit = qubits[1]
        ancillas = qubits[2:]
        measurement_key = 'TEST'
        measurer = FaultTolerantMeasurer(gates=[Z],
                                         targets=targets,
                                         measurement_qubit=measurement_qubit,
                                         ancillas=ancillas,
                                         measurement_key=measurement_key)
        circuit = measurer.get_measurement_circuit()

        initial_target_state = KET_PLUS_STATE_VECTOR
        initial_state = tensor(initial_target_state, *[KET_ZERO_STATE_VECTOR] * (len(qubits) - len(targets)))
        simulator = Simulator()

        num_trials = 5
        measurements = []
        for trial in range(num_trials):
            simulation = simulator.simulate(circuit, qubit_order=qubits, initial_state=initial_state)
            measurements.extend(simulation.measurements[measurement_key])
        assert any(measurements) and not all(measurements)

    def test_takes_majority_vote(self):
        qubits = LineQubit.range(3)
        targets = qubits[:1]
        measurement_qubit = qubits[1]
        ancillas = qubits[2:]
        measurement_key = 'TEST'
        measurer = FaultTolerantMeasurer(gates=[Z],
                                         targets=targets,
                                         measurement_qubit=measurement_qubit,
                                         ancillas=ancillas,
                                         measurement_key=measurement_key)
        circuit = measurer.get_measurement_circuit()

        simulator = Simulator()
        simulation = simulator.run(circuit)
        assert len(simulation.records) == 2
        assert allequal(simulation.records[measurement_key], [[[0]]])
        assert allequal(next(records for key, records in simulation.records.items() if key != measurement_key), [[[0], [0], [0,]]])

    def test_ensure_correct_number_of_ancillas(self):
        qubits = LineQubit.range(4)
        measurer = FaultTolerantMeasurer(gates=[X, X], targets=qubits[:2], measurement_qubit=qubits[2], ancillas=qubits[3:])
        with pytest.raises(ValueError, match="^The number of ancillas \\(1\\) must be at least the number of gates \\(2\\)\\.$"):
            measurer.get_measurement_circuit()

    def test_ensure_targets_and_measurement_are_disjoint(self):
        qubits = LineQubit.range(3)
        measurer = FaultTolerantMeasurer(gates=[X], targets=qubits[:1], measurement_qubit=qubits[0], ancillas=qubits[2:])
        with pytest.raises(ValueError, match="^The target qubits, measurement qubit, and ancilla qubits must be disjoint\\. "
                                             "Found duplicate qubit(s) {cirq.LineQubit\\(0\\)\\.$"):
            measurer.get_measurement_circuit()

    def test_ensure_targets_and_ancilla_are_disjoint(self):
        qubits = LineQubit.range(3)
        measurer = FaultTolerantMeasurer(gates=[X], targets=qubits[:1], measurement_qubit=qubits[1], ancillas=qubits[:1])
        with pytest.raises(ValueError, match="^The target qubits, measurement qubit, and ancilla qubits must be disjoint\\. "
                                             "Found duplicate qubit\\(s\\) {cirq.LineQubit\\(0\\)}\\.$"):
            measurer.get_measurement_circuit()

    def test_ensure_measaurement_and_ancilla_are_disjoint(self):
        qubits = LineQubit.range(3)
        measurer = FaultTolerantMeasurer(gates=[X], targets=qubits[:1], measurement_qubit=qubits[2],
                                         ancillas=qubits[2:])
        with pytest.raises(ValueError,
                           match="^The target qubits, measurement qubit, and ancilla qubits must be disjoint\\. "
                                 "Found duplicate qubit\\(s\\) {cirq.LineQubit\\(2\\)}\\.$"):
            measurer.get_measurement_circuit()

