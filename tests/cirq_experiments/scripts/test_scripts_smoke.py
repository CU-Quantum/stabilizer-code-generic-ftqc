import pytest

from cirq_experiments.scripts.deutsch_josza.deutsch_josza import DeutschJosza
from cirq_experiments.scripts.script_runner import RunnerConfiguration
from cirq_experiments.scripts.simple_measurement.simple_measurement import SimpleMeasurement
from cirq_experiments.scripts.universal_cnot.universal_cnot import UniversalCnot
from cirq_experiments.scripts.universal_hadamard.universal_hadamard import UniversalHadamard
from cirq_experiments.scripts.universal_t.universal_t import UniversalT


class TestScriptsSmoke:
    def test_simple_measurement_smoke(self):
        run_config = RunnerConfiguration(
            num_shots=1,
            surface_code_distance=3,
            num_measurement_rounds=3,
            depolarization_probability_one_qubit=0.001,
            depolarization_probability_two_qubit=0.002,
            num_processes=1,
        )
        SimpleMeasurement(run_configuration=run_config).run_main()

    def test_universal_cnot_smoke(self):
        run_config = RunnerConfiguration(
            num_shots=1,
            surface_code_distance=3,
            num_measurement_rounds=3,
            depolarization_probability_one_qubit=0.001,
            depolarization_probability_two_qubit=0.002,
            num_processes=1,
        )
        UniversalCnot(run_configuration=run_config).run_main()

    def test_universal_hadamard_smoke(self):
        run_config = RunnerConfiguration(
            num_shots=1,
            surface_code_distance=3,
            num_measurement_rounds=3,
            depolarization_probability_one_qubit=0.001,
            depolarization_probability_two_qubit=0.002,
            num_processes=1,
        )
        UniversalHadamard(run_configuration=run_config).run_main()

    def test_deutsch_josza_smoke(self):
        DeutschJosza(
            num_shots=1,
            num_input_qubits=2,
            surface_code_distance=3,
            is_balanced=False,
            num_measurement_rounds=3,
        ).run_main()

    @pytest.mark.skip(
        reason="Full state-vector simulation of the non-Clifford T gate requires high RAM (>2GB) and long runtime (>1 min)"
    )
    def test_universal_t_smoke(self):
        run_config = RunnerConfiguration(
            num_shots=1,
            surface_code_distance=3,
            num_measurement_rounds=3,
            depolarization_probability_one_qubit=0.001,
            depolarization_probability_two_qubit=0.002,
            num_processes=1,
        )
        UniversalT(run_configuration=run_config).run_main()
