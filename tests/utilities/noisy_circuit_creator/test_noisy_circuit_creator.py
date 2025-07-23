from cirq import CZ, Circuit, CircuitOperation, FrozenCircuit, I, LineQubit, Moment, TaggedOperation, Z, depolarize

from stim_experiments.custom_dataclasses.noise_parameters import NoiseParameters
from stim_experiments.custom_dataclasses.noisy_circuit import NoisyCircuit
from stim_experiments.globals.error_correcting_code_configuration import ConfigurationErrorCorrectingCodeManager
from stim_experiments.utilities.noisy_circuit_creator import NoisyCircuitCreator


class TestNoisyCircuitCreator:
    def test_trivial(self):
        circuit = Circuit()
        circuit_noisy = NoisyCircuitCreator(circuit=circuit, num_data_qubits=0).get_noisy_circuit()
        assert circuit_noisy == NoisyCircuit(
            circuit=Circuit(),
            num_noisy_operations=0,
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
            num_noisy_operations=1,
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
            num_noisy_operations=2,
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
            num_noisy_operations=2,
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
                    depolarize(p=self._depolarization_noise_one_qubit_gate).on(qubit) for qubit in qubits
                ),
                Moment(Z(qubits[0])),
                Moment(
                    depolarize(p=self._depolarization_noise_one_qubit_gate).on(qubit) for qubit in qubits
                ),
            ),
            num_noisy_operations=4,
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
                    depolarize(p=self._depolarization_noise_one_qubit_gate).on(qubit) for qubit in qubits
                ),
                Moment(CZ(qubits[0], qubits[1])),
                Moment(
                    [depolarize(p=self._depolarization_noise_two_qubit_gate).on(qubit) for qubit in qubits[:2]],
                    [depolarize(p=self._depolarization_noise_one_qubit_gate).on(qubit) for qubit in qubits[2:]]
                ),
            ),
            num_noisy_operations=6,
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
            num_noisy_operations=1,
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
            num_noisy_operations=1,
        )

    def test_noise_after_tagged_circuit_operation(self):
        qubits = LineQubit.range(3)
        circuit = Circuit(
            TaggedOperation(
                CircuitOperation(FrozenCircuit(Z(qubits[0]))),
                'TAG0'
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
                        'TAG0'
                    ),
                ),
            ),
            num_noisy_operations=1,
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
