from cmath import isclose

import pytest
from cirq import Circuit, LineQubit, MeasurementKey, X, Z

from stim_experiments.error_correcting_codes.support.measurer.measurer_with_single_qubit import MeasurerWithSingleQubit
from stim_experiments.globals.error_correcting_code_configuration import ConfigurationErrorCorrectingCodeManager
from stim_experiments.globals.fresh_ancillas_pool import FreshAncillasPool
from stim_experiments.simulations.error_correcting_runner import ErrorCorrectingRunnerClifford
from stim_experiments.utilities.noisy_circuit_creator import NoisyCircuitCreator


@pytest.mark.slow
class TestErrorRate:
    def test_error_rate(self):
        num_shots = 1000

        configuration = ConfigurationErrorCorrectingCodeManager().get_configuration()
        configuration.noise_parameters.depolarization_probability_one_qubit = 1e-2
        configuration.noise_parameters.depolarization_probability_two_qubit = 2e-2

        qubits = LineQubit.range(1)
        FreshAncillasPool().set_first_ancilla_num(first_ancilla_num=len(qubits))
        circuit = Circuit(
            X(qubits[0]),
            MeasurerWithSingleQubit(observables=[Z(qubits[0]), ], measurement_keys=MeasurementKey('0')).get_measurement_circuit()
        )
        circuit_noisy = NoisyCircuitCreator(circuit=circuit, num_data_qubits=len(qubits)).get_noisy_circuit()
        runner = ErrorCorrectingRunnerClifford(seed=0)
        result = runner.run_circuit(circuit=circuit_noisy.circuit, num_shots=num_shots)
        num_one_measurements = result.logical_qubit_measurements['0'].sum()
        percentage_of_one_measurements = num_one_measurements / num_shots
        expected_one_qubit_gate_errors = circuit_noisy.noisy_operations_count.one_qubit * ConfigurationErrorCorrectingCodeManager().get_configuration().noise_parameters.depolarization_probability_one_qubit
        expected_two_qubit_gate_errors = circuit_noisy.noisy_operations_count.two_qubit * ConfigurationErrorCorrectingCodeManager().get_configuration().noise_parameters.depolarization_probability_two_qubit
        assert isclose(percentage_of_one_measurements, 1, abs_tol=0.05)
