from typing import Optional

import pytest
from cirq import Circuit, CircuitOperation, Gate, I, LineQubit, NoiseModel, OP_TREE, Operation, Simulator, X

from stim_experiments.error_correcting_codes.error_correcting_code_utilities import get_error_correcting_code_utilities
from stim_experiments.error_correcting_codes.support.fault_tolerant_measurer.support.control_qubits_preparer import \
    ParityEnsurerCatState
from stim_experiments.utilities import KET_PLUS_STATE_VECTOR, KET_ZERO_STATE_VECTOR, tensor
from stim_experiments.error_correcting_codes.support.fault_tolerant_measurer.support.conditions.verification_is_zero import \
    VerificationIsZero
from tests.utilities import get_cat_state_vector, states_are_equal


class TestControlQubitsPreparer:
    @pytest.fixture(autouse=True)
    def _setup(self):
        self._num_target_qubits = 3
        self._num_ancilla_qubits = 1
        self._num_qubits = self._num_target_qubits + self._num_ancilla_qubits
        self._qubits = LineQubit.range(self._num_qubits)

        preparer = ParityEnsurerCatState(target_qubits=self._qubits[:-1], verifier_ancilla=self._qubits[-1])
        self._circuit_constructing_and_verifying_3_qubit_cat_state = preparer.prepare_state()

    def test_one_qubit_control(self):
        preparer = ParityEnsurerCatState(target_qubits=self._qubits[:1], verifier_ancilla=self._qubits[-1])
        circuit = preparer.prepare_state()
        simulation = Simulator().simulate(circuit, qubit_order=self._qubits)
        expected_state = tensor(KET_PLUS_STATE_VECTOR, *[KET_ZERO_STATE_VECTOR] * (len(self._qubits) - 1))
        assert states_are_equal(simulation.final_state_vector, expected_state)
        assert simulation.measurements == {}

    def test_creates_cat_state(self):
        circuit = self._circuit_constructing_and_verifying_3_qubit_cat_state
        assert self._successfully_created_3_qubit_cat_state(circuit=circuit, noise_model=None)
        assert self._number_of_repetitions(circuit=circuit) == 1

    def test_retries_if_invalid(self):
        circuit = self._circuit_constructing_and_verifying_3_qubit_cat_state
        assert self._successfully_created_3_qubit_cat_state(circuit=circuit, noise_model=BitFlipOnceNoiseModel())
        assert self._number_of_repetitions(circuit=circuit) == 2

    def _successfully_created_3_qubit_cat_state(self, circuit: Circuit, noise_model: Optional[NoiseModel]):
        initial_state = tensor(*[KET_ZERO_STATE_VECTOR] * self._num_qubits)
        error_correction_utilities = get_error_correcting_code_utilities(state=initial_state)

        state = error_correction_utilities.get_state_after_circuit(circuit=circuit,
                                                                   qubit_order=self._qubits,
                                                                   initial_state=initial_state,
                                                                   noise_model=noise_model)

        expected_target_qubits_state = get_cat_state_vector(num_qubits=self._num_target_qubits)
        expected_ancilla_qubits_state = tensor(*[KET_ZERO_STATE_VECTOR] * self._num_ancilla_qubits)
        return states_are_equal(state.state, tensor(expected_target_qubits_state, expected_ancilla_qubits_state))

    def _number_of_repetitions(self, circuit: Circuit) -> int:
        number_of_measurements_per_repetition = 2
        operation: CircuitOperation = circuit.moments[0].operations[0]
        resolver: VerificationIsZero = operation.repeat_until
        return resolver.last_num_measurements // number_of_measurements_per_repetition


class BitFlipOnceNoiseModel(NoiseModel):
    def __init__(self):
        super().__init__()
        self._added_noise = False

    def noisy_operation(self, operation: Operation) -> OP_TREE:
        circuit = operation.circuit.unfreeze()
        circuit.insert(1, BitFlipOnceChannel().on(operation.qubits[1]))
        return CircuitOperation(circuit.freeze(), use_repetition_ids=False, repeat_until=operation.repeat_until),


class BitFlipOnceChannel(Gate):
    def __init__(self):
        super().__init__()
        self._caused_bit_flip = False

    def _num_qubits_(self) -> int:
        return 1

    def _decompose_(self, qubits):
        target_qubit = qubits[0]
        if self._caused_bit_flip:
            yield I(target_qubit)
        else:
            yield X(target_qubit)
            self._caused_bit_flip = True
