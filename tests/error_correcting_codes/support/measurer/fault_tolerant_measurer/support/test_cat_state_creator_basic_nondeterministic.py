from typing import Optional

import pytest
from cirq import Circuit, CircuitOperation, Gate, I, LineQubit, NoiseModel, OP_TREE, Operation, X

from stim_experiments.error_correcting_codes.support.cat_state_creator.cat_state_creator_basic_nondeterministic import \
    CatStateCreatorBasicNondeterministic
from stim_experiments.globals.fresh_ancillas_pool import FreshAncillasPool
from stim_experiments.conditions.verification_is_zero import \
    VerificationIsZero
from stim_experiments.simulations.error_correcting_simulator import get_error_correcting_simulator
from stim_experiments.utilities.utilities import KET_ZERO_STATE_VECTOR, states_are_equal, tensor
from tests.utilities import get_cat_state_vector


class TestCatStateCreatorBasicNondeterministic:
    @pytest.fixture(autouse=True)
    def _setup(self):
        self._num_qubits = 3
        self._qubits = LineQubit.range(self._num_qubits)
        FreshAncillasPool().set_first_ancilla_num(first_ancilla_num=self._num_qubits)

        preparer = CatStateCreatorBasicNondeterministic(qubit_register=self._qubits)
        self._circuit_constructing_and_verifying_3_qubit_cat_state = preparer.get_cat_state_circuit()

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
        error_correction_utilities = get_error_correcting_simulator(state=initial_state)

        state = error_correction_utilities.get_state_after_circuit(circuit=circuit,
                                                                   num_data_qubits=self._num_qubits,
                                                                   initial_data_state=initial_state,
                                                                   noise_model=noise_model)

        expected_target_qubits_state = get_cat_state_vector(num_qubits=self._num_qubits)
        return states_are_equal(state.state, tensor(expected_target_qubits_state))

    def _number_of_repetitions(self, circuit: Circuit) -> int:
        number_of_measurements_per_repetition = 2
        operation: CircuitOperation = circuit.moments[0].operations[0]
        resolver: VerificationIsZero = operation.untagged.repeat_until
        return resolver._last_num_measurements // number_of_measurements_per_repetition


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
