from cirq import CZ, Circuit, CircuitOperation, FrozenCircuit, I, LineQubit, Moment, ResetChannel, TaggedOperation, Z, \
    depolarize

from stim_experiments.custom_dataclasses.noise_parameters import NoiseParameters
from stim_experiments.custom_dataclasses.noisy_circuit import NoisyCircuit
from stim_experiments.custom_dataclasses.noisy_operations_count import NoisyOperationsCountPerShot
from stim_experiments.error_correcting_codes.support.operations_applier.operations_applier import DELAYED_NOISE_TAG
from stim_experiments.globals.error_correcting_code_configuration import ConfigurationErrorCorrectingCodeManager
from stim_experiments.utilities.noisy_circuit_creator import NoisyCircuitCreator


class TestNoisyCircuitCreator:
    def test_trivial(self):
        circuit = Circuit()
        circuit_noisy = NoisyCircuitCreator(circuit=circuit, num_data_qubits=0).get_noisy_circuit()
        assert circuit_noisy == NoisyCircuit(
            circuit=Circuit(),
        )

    def test_noise_added_after_one_moment(self):
        qubits = LineQubit.range(1)
        circuit = Circuit(Moment(Z(qubits[0])))
        circuit_noisy = NoisyCircuitCreator(circuit=circuit, num_data_qubits=len(qubits)).get_noisy_circuit()
        assert circuit_noisy == NoisyCircuit(
            circuit=Circuit(
                Moment(Z(qubits[0])),
                Moment(depolarize(p=self._depolarization_noise_one_qubit_gate).on(qubits[0]))
            ),
            noisy_operations_count=NoisyOperationsCountPerShot(
                one_qubit=1,
            ),
        )

    def test_noise_added_after_two_moments(self):
        qubits = LineQubit.range(1)
        circuit = Circuit(Moment(Z(qubits[0])), Moment(Z(qubits[0])))
        circuit_noisy = NoisyCircuitCreator(circuit=circuit, num_data_qubits=len(qubits)).get_noisy_circuit()
        assert circuit_noisy == NoisyCircuit(
            circuit=Circuit(
                Moment(Z(qubits[0])),
                Moment(depolarize(p=self._depolarization_noise_one_qubit_gate).on(qubits[0])),
                Moment(Z(qubits[0])),
                Moment(depolarize(p=self._depolarization_noise_one_qubit_gate).on(qubits[0])),
            ),
            noisy_operations_count=NoisyOperationsCountPerShot(
                one_qubit=2,
            ),
        )

    def test_noise_added_after_one_moment_two_qubits(self):
        qubits = LineQubit.range(2)
        circuit = Circuit(Moment(Z(qubits[0]), Z(qubits[1])),)
        circuit_noisy = NoisyCircuitCreator(circuit=circuit, num_data_qubits=len(qubits)).get_noisy_circuit()
        assert circuit_noisy == NoisyCircuit(
            circuit=Circuit(
                Moment(Z(qubits[0]), Z(qubits[1])),
                Moment(
                    depolarize(p=self._depolarization_noise_one_qubit_gate).on(qubit) for qubit in qubits
                ),
            ),
            noisy_operations_count=NoisyOperationsCountPerShot(
                one_qubit=2,
            ),
        )

    def test_noise_on_inactive_qubits(self):
        qubits = LineQubit.range(2)
        circuit = Circuit(
            Moment(Z(qubits[0]), Z(qubits[1])),
            Moment(Z(qubits[0])),
        )
        circuit_noisy = NoisyCircuitCreator(circuit=circuit, num_data_qubits=len(qubits)).get_noisy_circuit()
        assert circuit_noisy == NoisyCircuit(
            circuit=Circuit(
                Moment(Z(qubits[0]), Z(qubits[1])),
                Moment(
                    depolarize(p=self._depolarization_noise_one_qubit_gate).on_each(*qubits)
                ),
                Moment(Z(qubits[0])),
                Moment(
                    depolarize(p=self._depolarization_noise_one_qubit_gate).on_each(*qubits)
                ),
            ),
            noisy_operations_count=NoisyOperationsCountPerShot(
                one_qubit=4,
            ),
        )

    def test_noise_on_inactive_qubits_after_two_qubit_gate(self):
        qubits = LineQubit.range(3)
        circuit = Circuit(
            Moment(Z(qubit) for qubit in qubits),
            Moment(CZ(qubits[0], qubits[1])),
        )
        circuit_noisy = NoisyCircuitCreator(circuit=circuit, num_data_qubits=len(qubits)).get_noisy_circuit()
        assert circuit_noisy == NoisyCircuit(
            circuit=Circuit(
                Moment(Z(qubits[0]), Z(qubits[1]), Z(qubits[2])),
                Moment(
                    depolarize(p=self._depolarization_noise_one_qubit_gate).on_each(*qubits)
                ),
                Moment(CZ(qubits[0], qubits[1])),
                Moment(
                    depolarize(p=self._depolarization_noise_two_qubit_gate).on_each(*qubits[:2]),
                    depolarize(p=self._depolarization_noise_one_qubit_gate).on_each(*qubits[2:]),
                ),
            ),
            noisy_operations_count=NoisyOperationsCountPerShot(
                one_qubit=4,
                two_qubit=2,
            ),
        )

    def test_noise_after_circuit_operation(self):
        qubits = LineQubit.range(3)
        circuit = Circuit(
            CircuitOperation(
                FrozenCircuit(Z(qubits[0]))
            )
        )
        circuit_noisy = NoisyCircuitCreator(circuit=circuit, num_data_qubits=len(qubits)).get_noisy_circuit()
        assert circuit_noisy == NoisyCircuit(
            circuit=Circuit(
                CircuitOperation(
                    FrozenCircuit(
                        Moment(Z(qubits[0])),
                        Moment(depolarize(p=self._depolarization_noise_one_qubit_gate).on(qubits[0]))
                    ),
                )
            ),
            noisy_operations_count=NoisyOperationsCountPerShot(
                one_qubit=1,
            ),
        )

    def test_noise_after_tagged_operation(self):
        qubits = LineQubit.range(3)
        circuit = Circuit(
            TaggedOperation(
                Z(qubits[0]),
                'TAG0'
            )
        )
        circuit_noisy = NoisyCircuitCreator(circuit=circuit, num_data_qubits=len(qubits)).get_noisy_circuit()
        assert circuit_noisy == NoisyCircuit(
            circuit=Circuit(
                Moment(
                    TaggedOperation(
                        Z(qubits[0]),
                        'TAG0'
                    ),
                ),
                Moment(depolarize(p=self._depolarization_noise_one_qubit_gate).on(qubits[0]))
            ),
            noisy_operations_count=NoisyOperationsCountPerShot(
                one_qubit=1,
            ),
        )

    def test_noise_after_tagged_circuit_operation(self):
        qubits = LineQubit.range(3)
        circuit = Circuit(
            TaggedOperation(
                CircuitOperation(FrozenCircuit(Z(qubits[0]))),
                'TAG_0'
            )
        )
        circuit_noisy = NoisyCircuitCreator(circuit=circuit, num_data_qubits=len(qubits)).get_noisy_circuit()
        assert circuit_noisy == NoisyCircuit(
            circuit=Circuit(
                Moment(
                    TaggedOperation(
                        CircuitOperation(
                            FrozenCircuit(
                                Moment(Z(qubits[0])),
                                Moment(depolarize(p=self._depolarization_noise_one_qubit_gate).on(qubits[0]))
                            ),
                        ),
                        'TAG_0'
                    ),
                ),
            ),
            noisy_operations_count=NoisyOperationsCountPerShot(
                one_qubit=1,
            ),
        )

    def test_delayed_noise_multiple_gates_and_idle_qubits(self):
        qubits = LineQubit.range(4)
        circuit = Circuit(
            I.on_each(*qubits),
            TaggedOperation(
                CircuitOperation(
                    FrozenCircuit(
                        Z(qubits[0]).controlled_by(qubits[2]),
                        Z(qubits[1]).controlled_by(qubits[2]),
                    )
                ),
                DELAYED_NOISE_TAG
            ),
        )
        circuit_noisy = NoisyCircuitCreator(circuit=circuit, num_data_qubits=4).get_noisy_circuit()
        assert circuit_noisy == NoisyCircuit(
            circuit=Circuit(
                I.on_each(*qubits),
                depolarize(p=self._depolarization_noise_one_qubit_gate).on_each(*qubits),
                TaggedOperation(
                    CircuitOperation(
                        FrozenCircuit(
                            Z(qubits[0]).controlled_by(qubits[2]),
                            Z(qubits[1]).controlled_by(qubits[2]),
                        )
                    ),
                    DELAYED_NOISE_TAG
                ),
                Moment(
                    depolarize(p=self._depolarization_noise_two_qubit_gate).on_each(qubits[:3]),
                    depolarize(p=self._depolarization_noise_one_qubit_gate).on(qubits[3])
                ),
            ),
            noisy_operations_count=NoisyOperationsCountPerShot(
                one_qubit=5,
                two_qubit=3
            ),
        )

    @property
    def _depolarization_noise_one_qubit_gate(self) -> float:
        return self._noise_parameters.depolarization_probability_one_qubit

    @property
    def _depolarization_noise_two_qubit_gate(self) -> float:
        return self._noise_parameters.depolarization_probability_two_qubit

    @property
    def _noise_parameters(self) -> NoiseParameters:
        return ConfigurationErrorCorrectingCodeManager().get_configuration().noise_parameters
