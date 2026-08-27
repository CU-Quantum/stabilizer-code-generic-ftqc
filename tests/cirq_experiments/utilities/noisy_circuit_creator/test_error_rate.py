from cmath import isclose

import pytest
from cirq import LineQubit

from cirq_experiments.algorithms.support.logical_operations_circuit_creator.logical_operations_circuit_creator import \
    LogicalOperationsCircuitCreator
from cirq_experiments.custom_dataclasses.transformation_operation import TransformationGate, TransformationOperation
from cirq_experiments.error_correcting_codes.repetition_code.repetition_code import RepetitionCodeOneLogical
from cirq_experiments.globals.error_correcting_code_configuration import ConfigurationErrorCorrectingCodeManager
from cirq_experiments.globals.fresh_ancillas_pool import FreshAncillasPool
from cirq_experiments.simulations.error_correcting_runner import ErrorCorrectingRunnerClifford
from cirq_experiments.utilities.noisy_circuit_creator import NoisyCircuitCreator


@pytest.mark.slow
@pytest.mark.very_slow(reason="Very long test (simulates 1000 noisy shots)")
class TestErrorRate:
    def test_error_rate(self):
        num_shots = 1000

        configuration = ConfigurationErrorCorrectingCodeManager().get_configuration()
        configuration.noise_parameters.depolarization_probability_one_qubit = 1e-2
        configuration.noise_parameters.depolarization_probability_two_qubit = 2e-2

        logical_qubit = RepetitionCodeOneLogical(num_qubits=3)
        qubits = LineQubit.range(len(logical_qubit.data_qubits))
        FreshAncillasPool().set_first_ancilla_num(first_ancilla_num=len(qubits))

        circuit = LogicalOperationsCircuitCreator(encodings=[logical_qubit], operations=[
            TransformationOperation(gate=TransformationGate.M, target_qubit_index=0),
        ]).get_simulation_circuit()
        circuit_noisy = NoisyCircuitCreator(circuit=circuit).get_noisy_circuit()
        runner = ErrorCorrectingRunnerClifford(seed=0)
        result = runner.run_circuit(circuit=circuit_noisy.circuit, num_shots=num_shots)
        num_one_measurements = result.logical_qubit_measurements['0'].sum()
        percentage_of_one_measurements = num_one_measurements / num_shots
        expected_one_qubit_gate_errors = circuit_noisy.noisy_operations_count.one_qubit * ConfigurationErrorCorrectingCodeManager().get_configuration().noise_parameters.depolarization_probability_one_qubit
        expected_two_qubit_gate_errors = circuit_noisy.noisy_operations_count.two_qubit * ConfigurationErrorCorrectingCodeManager().get_configuration().noise_parameters.depolarization_probability_two_qubit
        assert isclose(percentage_of_one_measurements, 1, abs_tol=0.05)
