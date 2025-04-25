from typing import Optional

import numpy.random
import pytest
from cirq import Circuit, Gate, LineQubit, M, Simulator, X, Z, inverse

from stim_experiments.utilities import KET_PLUS_STATE_VECTOR, KET_ZERO_STATE_VECTOR, tensor
from tests.error_correcting_codes.support.fault_tolerant_measurer.support.test_cat_state_circuit_creator import \
    CatStateCircuitCreator
from tests.error_correcting_codes.support.fault_tolerant_measurer.support.test_control_qubits_preparer import \
    ControlQubitsPreparer
from tests.error_correcting_codes.support.fault_tolerant_measurer.support.test_controlled_single_qubit_gates_applier import \
    ControlledSingleQubitGatesApplier


class FaultTolerantMeasurer:
    def __init__(self,
                 gates: list[Gate],
                 targets: list[LineQubit],
                 measurement_qubit: LineQubit,
                 ancillas: list[LineQubit],
                 measurement_key: Optional[str] = None,
                 ):
        self._gates = gates
        self._targets = targets
        self._measurement_qubit = measurement_qubit
        self._ancillas = ancillas
        self._measurement_key = measurement_key

    def get_measurement_circuit(self) -> Circuit:
        self._validate()
        return Circuit(
            ControlQubitsPreparer(target_qubits=self._control, verifier_ancilla=self._verifier_ancilla).prepare_state(),
            ControlledSingleQubitGatesApplier(gates=self._gates, targets=self._targets, controls=self._control).get_circuit(),
            inverse(CatStateCircuitCreator(target_qubits=self._control).create_circuit()),
            M(self._measurement_qubit, key=self._measurement_key),
        )

    def _validate(self) -> None:
        if len(self._ancillas) < len(self._gates):
            raise ValueError(
                f"The number of ancillas ({len(self._ancillas)}) must be at least the number of gates ({len(self._gates)}).")
        qubits = self._targets + [self._measurement_qubit] + self._ancillas
        qubits_set = set(qubits)
        if len(qubits) != len(qubits_set):
            duplicates = qubits.copy()
            for qubit in qubits_set:
                duplicates.remove(qubit)
            raise ValueError(f"The target qubits, measurement qubit, and ancilla qubits must be disjoint. "
                             f"Found duplicate qubit(s) {set(duplicates)}.")

    @property
    def _control(self) -> list[LineQubit]:
        return [self._measurement_qubit] + self._ancillas[:len(self._gates) - 1]

    @property
    def _verifier_ancilla(self) -> LineQubit:
        return self._ancillas[-1]


class TestFaultTolerantMeasurer:
    def test_trivial(self):
        measurer = FaultTolerantMeasurer(gates=[], targets=[], control=[], verifier_ancilla=LineQubit(0))
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

