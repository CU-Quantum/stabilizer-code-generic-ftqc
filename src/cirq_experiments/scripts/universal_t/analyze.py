from cirq_experiments.scripts.analyzer import Analyzer
from cirq_experiments.scripts.script_runner import RunnerConfiguration
from cirq_experiments.scripts.universal_t.universal_t import UniversalT

if __name__ == '__main__':
    run_config = RunnerConfiguration(
        num_shots=1,
        surface_code_distance=3,
        num_measurement_rounds=3,
        depolarization_probability_one_qubit=1e-3,
        depolarization_probability_two_qubit=2e-3,
        num_processes=1,
    )
    universal_t = UniversalT(run_configuration=run_config)
    Analyzer(
        filepath=__file__,
        was_successful=universal_t.was_successful,
        is_state_vector=True,
        num_data_qubits=len(universal_t.script_runner.circuit_creator.data_qubits),
    ).analyze()
