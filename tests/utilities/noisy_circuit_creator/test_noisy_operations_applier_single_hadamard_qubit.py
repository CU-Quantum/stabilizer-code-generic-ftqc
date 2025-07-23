from cirq import Circuit, CircuitOperation, FrozenCircuit, H, LineQubit, Moment, ResetChannel, TaggedOperation, X, Z, \
    depolarize

from stim_experiments.custom_dataclasses.noise_parameters import NoiseParameters
from stim_experiments.custom_dataclasses.noisy_circuit import NoisyCircuit
from stim_experiments.error_correcting_codes.support.operations_applier.operations_applier import NO_NOISE_TAG
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
                Z(qubits[0]).controlled_by(qubits[1]),
                Moment(depolarize(p=self._depolarization_noise_two_qubit_gate).on_each(*qubits)),
                H(qubits[1]),
                Moment(depolarize(p=self._depolarization_noise_one_qubit_gate).on_each(*qubits)),
                ResetChannel().on_each(qubits[1])
            ),
            num_noisy_operations=6,
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
                    NO_NOISE_TAG
                ),
                H(qubits[2]),
                Moment(depolarize(p=self._depolarization_noise_one_qubit_gate).on_each(*qubits)),
                ResetChannel().on_each(qubits[2])
            ),
            num_noisy_operations=6,
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
