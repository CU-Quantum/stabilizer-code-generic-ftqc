from cirq import Circuit, LineQubit

from stim_experiments.error_correcting_codes.support.operations_applier.operations_applier_using_single_qubit_hadamard_control import \
    OperationsApplierUsingSingleQubitHadamardControl
from stim_experiments.utilities.noisy_circuit_creator import NoisyCircuitCreator


class TestNoisyOperationsApplierSingleHadamardQubit:
    def test_trivial(self):
        applier = OperationsApplierUsingSingleQubitHadamardControl(operations=[], measurement_qubit=LineQubit(0))
        circuit = applier.get_application_circuit()
        circuit_noisy = NoisyCircuitCreator(circuit=circuit, num_data_qubits=0).get_noisy_circuit()
        assert circuit == Circuit()
