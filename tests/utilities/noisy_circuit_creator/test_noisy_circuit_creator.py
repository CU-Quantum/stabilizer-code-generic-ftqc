from cirq import Circuit, I, LineQubit, Moment, Z, depolarize

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
                Moment(depolarize(p=self._depolarization_noise_one_qubit_gate).on(qubits[0]))),
            num_noisy_operations=1,
        )

    @property
    def _depolarization_noise_one_qubit_gate(self) -> float:
        return ConfigurationErrorCorrectingCodeManager().get_configuration().noise_parameters.depolarization_probability_one_qubit
