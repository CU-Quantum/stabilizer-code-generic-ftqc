from abc import ABC, abstractmethod
from typing import Optional

from cirq import CliffordSimulator, NOISE_MODEL_LIKE, Result
from qsimcirq.qsim_avx2 import Circuit

from custom_dataclasses.state_and_measurements import Measurements


class ErrorCorrectingRunner(ABC):
    @abstractmethod
    def run_circuit(self, circuit: Circuit, num_shots: int, noise_model: Optional[NOISE_MODEL_LIKE] = None) -> Measurements:
        pass


class ErrorCorrectingRunnerClifford(ErrorCorrectingRunner):
    def run_circuit(self, circuit: Circuit, num_shots: int, noise_model: Optional[NOISE_MODEL_LIKE] = None) -> Measurements:
        circuit_noisy = circuit.with_noise(noise_model) if noise_model else circuit  # TODO apply noise model to CircuitOperations and FrozenCircuits
        simulator = CliffordSimulator()
        result: Result = simulator.run(circuit_noisy, repetitions=num_shots)
        return Measurements(measurements=dict(result.records))
