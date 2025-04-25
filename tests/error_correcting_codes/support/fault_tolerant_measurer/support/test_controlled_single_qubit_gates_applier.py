import pytest
from cirq import CX, Circuit, Gate, H, LineQubit, Simulator, X

from stim_experiments.utilities import KET_ONE_STATE_VECTOR, KET_PLUS_STATE_VECTOR, KET_ZERO_STATE_VECTOR, \
    TYPE_STATE_VECTOR, tensor
from tests.utilities import states_are_equal


class ControlledSingleQubitGatesApplier:
    def __init__(self, gates: list[Gate], targets: list[LineQubit], controls: list[LineQubit]):
        self._gates = gates
        self._targets = targets
        self._controls = controls

    def get_circuit(self) -> Circuit:
        self._validate_inputs()
        return Circuit(
            self._gates[i].on(self._targets[i]).controlled_by(self._controls[i])
            for i in range(len(self._gates))
        )

    def _validate_inputs(self) -> None:
        if len(self._gates) != len(self._targets) or len(self._gates) != len(self._controls):
            raise ValueError(
                f"The number of gates ({len(self._gates)}), targets ({len(self._targets)}), and controls({len(self._controls)}) must be equal.")
        if any(gate.num_qubits() != 1 for gate in self._gates):
            raise ValueError(f"All gates must be single-qubit gates. Was given {self._gates}.")


class TestControlledSingleQubitGatesApplier:
    def test_trivial(self):
        applier = ControlledSingleQubitGatesApplier(gates=[], targets=[], controls=[])
        circuit = applier.get_circuit()
        assert circuit == Circuit()

    @pytest.mark.parametrize('initial_control_state', [KET_ZERO_STATE_VECTOR, KET_ONE_STATE_VECTOR])
    def test_one_x_gate(self, initial_control_state: TYPE_STATE_VECTOR):
        qubits = LineQubit.range(2)
        applier = ControlledSingleQubitGatesApplier(gates=[X], targets=[qubits[0]], controls=[qubits[1]])
        circuit = applier.get_circuit()

        initial_state = tensor(KET_ZERO_STATE_VECTOR, initial_control_state)
        simulation = Simulator().simulate(circuit, initial_state=initial_state, qubit_order=qubits)
        expected_state = tensor(initial_control_state, initial_control_state)
        assert states_are_equal(simulation.final_state_vector, expected_state)

    def test_unequal_number_of_gates(self):
        qubits = LineQubit.range(4)
        applier = ControlledSingleQubitGatesApplier(gates=[X], targets=qubits[:2], controls=qubits[2:])
        with pytest.raises(ValueError, match="^The number of gates \\(1\\), targets \\(2\\), and controls\\(2\\) must be equal\\.$"):
            applier.get_circuit()

    def test_unequal_number_of_targets(self):
        qubits = LineQubit.range(3)
        applier = ControlledSingleQubitGatesApplier(gates=[X, X], targets=qubits[:1], controls=qubits[1:])
        with pytest.raises(ValueError, match="^The number of gates \\(2\\), targets \\(1\\), and controls\\(2\\) must be equal\\.$"):
            applier.get_circuit()

    def test_unequal_number_of_controls(self):
        qubits = LineQubit.range(3)
        applier = ControlledSingleQubitGatesApplier(gates=[X, X], targets=qubits[:2], controls=qubits[2:])
        with pytest.raises(ValueError, match="^The number of gates \\(2\\), targets \\(2\\), and controls\\(1\\) must be equal\\.$"):
            applier.get_circuit()

    def test_ensures_only_single_qubit_gates(self):
        qubits = LineQubit.range(2)
        applier = ControlledSingleQubitGatesApplier(gates=[CX], targets=qubits[:1], controls=qubits[1:])
        with pytest.raises(ValueError, match="^All gates must be single-qubit gates\\. Was given \\[cirq\\.CNOT\\]\\.$"):
            applier.get_circuit()

    @pytest.mark.parametrize('initial_control_state, expected_data_state', [
        (tensor(KET_ZERO_STATE_VECTOR, KET_ZERO_STATE_VECTOR), tensor(KET_ZERO_STATE_VECTOR, KET_ZERO_STATE_VECTOR)),
        (tensor(KET_ONE_STATE_VECTOR, KET_ONE_STATE_VECTOR), tensor(KET_PLUS_STATE_VECTOR, KET_ONE_STATE_VECTOR)),
    ])
    def test_two_gates_h_and_x(self, initial_control_state: TYPE_STATE_VECTOR, expected_data_state: TYPE_STATE_VECTOR):
        qubits = LineQubit.range(4)
        applier = ControlledSingleQubitGatesApplier(gates=[H, X], targets=qubits[:2], controls=qubits[2:])
        circuit = applier.get_circuit()

        initial_state = tensor(KET_ZERO_STATE_VECTOR, KET_ZERO_STATE_VECTOR, initial_control_state)
        simulation = Simulator().simulate(circuit, initial_state=initial_state, qubit_order=qubits)
        expected_state = tensor(expected_data_state, initial_control_state)
        assert states_are_equal(simulation.final_state_vector, expected_state)
