import pytest
import stim
from sinter import TaskStats

from stim_experiments.simulate_cx.custom_dataclasses import RunConfiguration
from stim_experiments.simulate_cx.simulate_cx import SimulateCx
from stim_experiments.simulate_cx.support.stabilizer_code_utilities import (
    get_five_qubit_code_utilities,
    get_dodecacode_utilities,
)


class TestSimulateCxSmoke:
    def test_five_qubit_smoke(self):
        target_code = get_five_qubit_code_utilities()
        run_config = RunConfiguration(
            max_shots=10,
            max_errors=5,
            depolarization_probabilities=[0.01],
            num_workers=1,
        )
        sim = SimulateCx(
            num_cat_states=3,
            target_code_utilities=target_code,
            si=0,
            run_configuration=run_config,
        )
        samples = sim.run_main()
        assert len(samples) == 1
        assert isinstance(samples[0], TaskStats)
        assert samples[0].shots > 0

    def test_bare_circuit_smoke(self):
        target_code = get_five_qubit_code_utilities()
        circuit = SimulateCx.build_bare_circuit(
            target_code=target_code,
            physical_error_rate=0.001,
            num_rounds=3,
        )
        assert isinstance(circuit, stim.Circuit)
        assert len(circuit) > 0

    def test_bare_circuit_all_measured_smoke(self):
        target_code = get_five_qubit_code_utilities()
        circuit = SimulateCx.build_bare_circuit_all_measured(
            target_code=target_code,
            physical_error_rate=0.001,
            num_rounds=3,
        )
        assert isinstance(circuit, stim.Circuit)
        assert len(circuit) > 0
