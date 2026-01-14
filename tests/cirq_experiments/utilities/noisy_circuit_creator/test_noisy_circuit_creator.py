from cirq import CZ, Circuit, CircuitOperation, FrozenCircuit, I, LineQubit, Moment, TaggedOperation, X, Y, Z, \
    depolarize

from cirq_experiments.custom_dataclasses.noise_parameters import NoiseParameters
from cirq_experiments.custom_dataclasses.noisy_circuit import NoisyCircuit
from cirq_experiments.custom_dataclasses.noisy_operations_count import NoisyOperationsCountPerCorrectionRound, \
    NoisyOperationsCountPerShot
from cirq_experiments.support.operations_applier.operations_applier import DELAYED_NOISE_TAG
from cirq_experiments.globals.error_correcting_code_configuration import ConfigurationErrorCorrectingCodeManager
from cirq_experiments.utilities.noisy_circuit_creator import NoisyCircuitCreator


POSSIBLE_ERRORS = (I, X, Y, Z)


class TestNoisyCircuitCreator:
    def test_trivial(self):
        circuit = Circuit()
        circuit_noisy = NoisyCircuitCreator(circuit=circuit).get_noisy_circuit()
        assert circuit_noisy == NoisyCircuit(
            circuit=Circuit(),
        )

    def test_noise_added_after_one_moment(self):
        qubits = LineQubit.range(1)
        circuit = Circuit(Moment(Z(qubits[0])))
        circuit_noisy = NoisyCircuitCreator(circuit=circuit).get_noisy_circuit()
        count = circuit_noisy.noisy_operations_count.counts[0]
        assert circuit_noisy.circuit in [
            Circuit(
                Moment(Z(qubits[0])),
                Moment(
                    TaggedOperation(possible_error(LineQubit(0)), 'NoisyChannel', 'NoisyChannel_OneQubit'),
                ),
            )
            for possible_error in POSSIBLE_ERRORS
        ]
        assert len(circuit_noisy.noisy_operations_count.counts) == 1
        assert count.one_qubit == 1
        assert not count.two_qubit
        assert count.i_errors.count + count.x_errors.count + count.y_errors.count + count.z_errors.count == count.one_qubit

    def test_noise_added_after_two_moments(self):
        qubits = LineQubit.range(1)
        circuit = Circuit(Moment(Z(qubits[0])), Moment(Z(qubits[0])))
        circuit_noisy = NoisyCircuitCreator(circuit=circuit).get_noisy_circuit()
        count = circuit_noisy.noisy_operations_count.counts[0]
        assert circuit_noisy.circuit in [
            Circuit(
                Moment(Z(qubits[0])),
                Moment(
                    TaggedOperation(possible_error0(LineQubit(0)), 'NoisyChannel', 'NoisyChannel_OneQubit'),
                ),
                Moment(Z(qubits[0])),
                Moment(
                    TaggedOperation(possible_error1(LineQubit(0)), 'NoisyChannel', 'NoisyChannel_OneQubit'),
                ),
            )
            for possible_error0 in POSSIBLE_ERRORS for possible_error1 in POSSIBLE_ERRORS
        ]
        assert len(circuit_noisy.noisy_operations_count.counts) == 1
        assert count.one_qubit == 2
        assert not count.two_qubit
        assert count.i_errors.count + count.x_errors.count + count.y_errors.count + count.z_errors.count == count.one_qubit

    def test_noise_added_after_one_moment_two_qubits(self):
        qubits = LineQubit.range(2)
        circuit = Circuit(Moment(Z(qubits[0]), Z(qubits[1])),)
        circuit_noisy = NoisyCircuitCreator(circuit=circuit).get_noisy_circuit()
        count = circuit_noisy.noisy_operations_count.counts[0]
        assert circuit_noisy.circuit in [
            Circuit(
                Moment(Z(qubits[0]), Z(qubits[1])),
                Moment(
                    TaggedOperation(possible_error0(LineQubit(0)), 'NoisyChannel', 'NoisyChannel_OneQubit'),
                    TaggedOperation(possible_error1(LineQubit(1)), 'NoisyChannel', 'NoisyChannel_OneQubit'),
                ),
            )
            for possible_error0 in POSSIBLE_ERRORS for possible_error1 in POSSIBLE_ERRORS
        ]
        assert len(circuit_noisy.noisy_operations_count.counts) == 1
        assert count.one_qubit == 2
        assert not count.two_qubit
        assert count.i_errors.count + count.x_errors.count + count.y_errors.count + count.z_errors.count == count.one_qubit

    def test_noise_on_inactive_qubits(self):
        qubits = LineQubit.range(2)
        circuit = Circuit(
            Moment(Z(qubits[0]), Z(qubits[1])),
            Moment(Z(qubits[0])),
        )
        circuit_noisy = NoisyCircuitCreator(circuit=circuit).get_noisy_circuit()
        count = circuit_noisy.noisy_operations_count.counts[0]
        assert circuit_noisy.circuit in [
            Circuit(
                Moment(Z(qubits[0]), Z(qubits[1])),
                Moment(
                    TaggedOperation(possible_error0(LineQubit(0)), 'NoisyChannel', 'NoisyChannel_OneQubit'),
                    TaggedOperation(possible_error1(LineQubit(1)), 'NoisyChannel', 'NoisyChannel_OneQubit'),
                ),
                Moment(Z(qubits[0])),
                Moment(
                    TaggedOperation(possible_error2(LineQubit(0)), 'NoisyChannel', 'NoisyChannel_OneQubit'),
                    TaggedOperation(possible_error3(LineQubit(1)), 'NoisyChannel', 'NoisyChannel_OneQubit'),
                ),
            )
            for possible_error0 in POSSIBLE_ERRORS for possible_error1 in POSSIBLE_ERRORS for possible_error2 in POSSIBLE_ERRORS for possible_error3 in POSSIBLE_ERRORS
        ]
        assert len(circuit_noisy.noisy_operations_count.counts) == 1
        assert count.one_qubit == 4
        assert not count.two_qubit
        assert count.i_errors.count + count.x_errors.count + count.y_errors.count + count.z_errors.count == count.one_qubit

    def test_noise_on_inactive_qubits_after_two_qubit_gate(self):
        qubits = LineQubit.range(3)
        circuit = Circuit(
            Moment(Z(qubit) for qubit in qubits),
            Moment(CZ(qubits[0], qubits[1])),
        )
        circuit_noisy = NoisyCircuitCreator(circuit=circuit).get_noisy_circuit()
        count = circuit_noisy.noisy_operations_count.counts[0]
        assert len(circuit_noisy.noisy_operations_count.counts) == 1
        assert count.one_qubit == 4
        assert count.two_qubit == 2
        assert count.i_errors.count + count.x_errors.count + count.y_errors.count + count.z_errors.count == count.one_qubit + count.two_qubit

    def test_noise_after_circuit_operation(self):
        qubits = LineQubit.range(1)
        circuit = Circuit(
            CircuitOperation(
                FrozenCircuit(Z(qubits[0]))
            )
        )
        circuit_noisy = NoisyCircuitCreator(circuit=circuit).get_noisy_circuit()
        count = circuit_noisy.noisy_operations_count.counts[0]
        assert circuit_noisy.circuit in [
            Circuit(
                Moment(
                    CircuitOperation(
                        FrozenCircuit(
                            Moment(Z(qubits[0])),
                            Moment(
                                TaggedOperation(possible_error0(LineQubit(0)), 'NoisyChannel', 'NoisyChannel_OneQubit'),
                            ),
                        ),
                    ),
                ),
            )
            for possible_error0 in POSSIBLE_ERRORS
        ]
        assert len(circuit_noisy.noisy_operations_count.counts) == 1
        assert count.one_qubit == 1
        assert count.two_qubit == 0
        assert count.i_errors.count + count.x_errors.count + count.y_errors.count + count.z_errors.count == count.one_qubit + count.two_qubit

    def test_noise_after_tagged_operation(self):
        qubits = LineQubit.range(3)
        circuit = Circuit(
            TaggedOperation(
                Z(qubits[0]),
                'TAG0'
            )
        )
        circuit_noisy = NoisyCircuitCreator(circuit=circuit).get_noisy_circuit()
        count = circuit_noisy.noisy_operations_count.counts[0]
        assert circuit_noisy.circuit in [
            Circuit(
                FrozenCircuit(
                    Moment(
                        TaggedOperation(Z(qubits[0]), 'TAG0'),
                    ),
                    Moment(
                        TaggedOperation(possible_error0(LineQubit(0)), 'NoisyChannel', 'NoisyChannel_OneQubit'),
                    ),
                ),
            )
            for possible_error0 in POSSIBLE_ERRORS
        ]
        assert len(circuit_noisy.noisy_operations_count.counts) == 1
        assert count.one_qubit == 1
        assert count.two_qubit == 0
        assert count.i_errors.count + count.x_errors.count + count.y_errors.count + count.z_errors.count == count.one_qubit + count.two_qubit

    def test_noise_after_tagged_circuit_operation(self):
        qubits = LineQubit.range(3)
        circuit = Circuit(
            TaggedOperation(
                CircuitOperation(FrozenCircuit(Z(qubits[0]))),
                'TAG_0'
            )
        )
        circuit_noisy = NoisyCircuitCreator(circuit=circuit).get_noisy_circuit()
        count = circuit_noisy.noisy_operations_count.counts[0]
        assert circuit_noisy.circuit in [
            Circuit(
                Moment(
                    TaggedOperation(
                        CircuitOperation(
                            FrozenCircuit(
                                Moment(Z(qubits[0])),
                                Moment(
                                    TaggedOperation(possible_error0(LineQubit(0)), 'NoisyChannel', 'NoisyChannel_OneQubit'),
                                ),
                            ),
                        ),
                        'TAG_0'
                    )
                ),
            )
            for possible_error0 in POSSIBLE_ERRORS
        ]
        assert len(circuit_noisy.noisy_operations_count.counts) == 1
        assert count.one_qubit == 1
        assert count.two_qubit == 0
        assert count.i_errors.count + count.x_errors.count + count.y_errors.count + count.z_errors.count == count.one_qubit + count.two_qubit

    # TODO: here is where errors are doubled (re: both single- and double- qubit gates)
    def test_delayed_noise_multiple_gates_and_idle_qubits(self):
        qubits = LineQubit.range(4)
        circuit = Circuit(
            TaggedOperation(
                CircuitOperation(
                    FrozenCircuit(
                        I.on_each(*qubits),
                        Z(qubits[0]).controlled_by(qubits[2]),
                        Z(qubits[1]).controlled_by(qubits[2]),
                    )
                ),
                DELAYED_NOISE_TAG
            ),
        )
        circuit_noisy = NoisyCircuitCreator(circuit=circuit).get_noisy_circuit()
        count = circuit_noisy.noisy_operations_count.counts[0]
        assert circuit_noisy.circuit in [
            Circuit(
                Moment(
                    TaggedOperation(
                        CircuitOperation(
                            FrozenCircuit(
                                I.on_each(*qubits),
                                Z(qubits[0]).controlled_by(qubits[2]),
                                Z(qubits[1]).controlled_by(qubits[2]),
                            ),
                        ),
                        DELAYED_NOISE_TAG
                    )
                ),
                Moment(
                    TaggedOperation(possible_error0(LineQubit(0)), 'NoisyChannel', 'NoisyChannel_OneQubit'),
                    TaggedOperation(possible_error1(LineQubit(1)), 'NoisyChannel', 'NoisyChannel_OneQubit'),
                    TaggedOperation(possible_error2(LineQubit(2)), 'NoisyChannel', 'NoisyChannel_OneQubit'),
                    TaggedOperation(possible_error3(LineQubit(3)), 'NoisyChannel', 'NoisyChannel_OneQubit'),
                ),
                Moment(
                    TaggedOperation(possible_error0(LineQubit(0)), 'NoisyChannel', 'NoisyChannel_TwoQubit'),
                    TaggedOperation(possible_error1(LineQubit(1)), 'NoisyChannel', 'NoisyChannel_TwoQubit'),
                    TaggedOperation(possible_error2(LineQubit(2)), 'NoisyChannel', 'NoisyChannel_TwoQubit'),
                ),
            )
            for possible_error0 in POSSIBLE_ERRORS for possible_error1 in POSSIBLE_ERRORS for possible_error2 in POSSIBLE_ERRORS for possible_error3 in POSSIBLE_ERRORS
        ]
        assert len(circuit_noisy.noisy_operations_count.counts) == 1
        assert count.one_qubit == 4
        assert count.two_qubit == 3
        assert count.i_errors.count + count.x_errors.count + count.y_errors.count + count.z_errors.count == count.one_qubit + count.two_qubit

    @property
    def _depolarization_noise_one_qubit_gate(self) -> float:
        return self._noise_parameters.depolarization_probability_one_qubit

    @property
    def _depolarization_noise_two_qubit_gate(self) -> float:
        return self._noise_parameters.depolarization_probability_two_qubit

    @property
    def _noise_parameters(self) -> NoiseParameters:
        return ConfigurationErrorCorrectingCodeManager().get_configuration().noise_parameters
