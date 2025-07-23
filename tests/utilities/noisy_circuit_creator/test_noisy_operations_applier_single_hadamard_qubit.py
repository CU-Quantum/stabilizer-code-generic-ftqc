from cirq import Circuit, CircuitOperation, FrozenCircuit, H, I, LineQubit, Moment, ResetChannel, TaggedOperation, X, Z, \
    depolarize

from stim_experiments.custom_dataclasses.noise_parameters import NoiseParameters
from stim_experiments.custom_dataclasses.noisy_circuit import NoisyCircuit
from stim_experiments.custom_dataclasses.noisy_operations_count import NoisyOperationsCount
from stim_experiments.error_correcting_codes.support.operations_applier.operations_applier import DELAYED_NOISE_TAG
from stim_experiments.error_correcting_codes.support.operations_applier.operations_applier_using_single_qubit_hadamard_control import \
    OperationsApplierUsingSingleQubitHadamardControl
from stim_experiments.globals.error_correcting_code_configuration import ConfigurationErrorCorrectingCodeManager
from stim_experiments.utilities.noisy_circuit_creator import NoisyCircuitCreator


class TestNoisyOperationsApplierSingleHadamardQubit:
    def test_one_operation(self):
        qubits = LineQubit.range(2)
        applier = OperationsApplierUsingSingleQubitHadamardControl(operations=[
            Z(qubits[0])
        ], measurement_qubit=qubits[1])
        circuit = applier.get_application_circuit()
        circuit_noisy = NoisyCircuitCreator(circuit=circuit, num_data_qubits=1).get_noisy_circuit()
        assert circuit_noisy == NoisyCircuit(
            circuit=Circuit(
                H(qubits[1]),
                Moment(depolarize(p=self._depolarization_noise_one_qubit_gate).on_each(*qubits)),
                TaggedOperation(
                    CircuitOperation(
                        FrozenCircuit(
                            Z(qubits[0]).controlled_by(qubits[1]),
                        )
                    ),
                    DELAYED_NOISE_TAG
                ),
                Moment(depolarize(p=self._depolarization_noise_two_qubit_gate).on_each(*qubits)),
                H(qubits[1]),
                Moment(depolarize(p=self._depolarization_noise_one_qubit_gate).on_each(*qubits)),
                ResetChannel().on_each(qubits[1])
            ),
            noisy_operations_count=NoisyOperationsCount(
                one_qubit=4,
                two_qubit=2
            )
        )

    def test_two_operations(self):
        qubits = LineQubit.range(3)
        applier = OperationsApplierUsingSingleQubitHadamardControl(operations=[
            Z(qubits[0]),
            X(qubits[1])
        ], measurement_qubit=qubits[2])
        circuit = applier.get_application_circuit()
        circuit_noisy = NoisyCircuitCreator(circuit=circuit, num_data_qubits=2).get_noisy_circuit()
        assert circuit_noisy == NoisyCircuit(
            circuit=Circuit(
                H(qubits[2]),
                Moment(depolarize(p=self._depolarization_noise_one_qubit_gate).on_each(*qubits)),
                TaggedOperation(
                    CircuitOperation(
                        FrozenCircuit(
                            Z(qubits[0]).controlled_by(qubits[2]),
                            X(qubits[1]).controlled_by(qubits[2]),
                        )
                    ),
                    DELAYED_NOISE_TAG
                ),
                Moment(depolarize(p=self._depolarization_noise_two_qubit_gate).on_each(*qubits)),
                H(qubits[2]),
                Moment(depolarize(p=self._depolarization_noise_one_qubit_gate).on_each(*qubits)),
                ResetChannel().on_each(qubits[2])
            ),
            noisy_operations_count=NoisyOperationsCount(
                one_qubit=6,
                two_qubit=3
            )
        )

    def test_noise_on_idle_qubits(self):
        qubits = LineQubit.range(3)
        applier = OperationsApplierUsingSingleQubitHadamardControl(operations=[
            Z(qubits[0]),
        ], measurement_qubit=qubits[2])
        circuit = Circuit(
            I.on_each(*qubits),
            applier.get_application_circuit()
        )
        circuit_noisy = NoisyCircuitCreator(circuit=circuit, num_data_qubits=2).get_noisy_circuit()
        assert circuit_noisy == NoisyCircuit(
            circuit=Circuit(
                I.on_each(*qubits),
                Moment(depolarize(p=self._depolarization_noise_one_qubit_gate).on_each(*qubits)),
                H(qubits[2]),
                Moment(depolarize(p=self._depolarization_noise_one_qubit_gate).on_each(*qubits)),
                TaggedOperation(
                    CircuitOperation(
                        FrozenCircuit(
                            Z(qubits[0]).controlled_by(qubits[2]),
                        )
                    ),
                    DELAYED_NOISE_TAG
                ),
                Moment(
                    depolarize(p=self._depolarization_noise_two_qubit_gate).on_each(*qubits[:1] + qubits[2:]),
                    depolarize(p=self._depolarization_noise_one_qubit_gate).on(qubits[1]),
                ),
                H(qubits[2]),
                Moment(depolarize(p=self._depolarization_noise_one_qubit_gate).on_each(*qubits)),
                ResetChannel().on_each(qubits[2])
            ),
            noisy_operations_count=NoisyOperationsCount(
                one_qubit=10,
                two_qubit=2
            )
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
