from typing import Sequence

from cirq import Circuit, Moment, Operation, Qid, depolarize, map_moments

from stim_experiments.custom_dataclasses.noise_parameters import NoiseParameters
from stim_experiments.custom_dataclasses.noisy_circuit import NoisyCircuit
from stim_experiments.globals.error_correcting_code_configuration import ConfigurationErrorCorrectingCodeManager


# TODO dont insert noise during sequential measurement
class NoisyCircuitCreator:
    def __init__(self, circuit: Circuit):
        self._circuit = circuit
        self._num_noisy_operations = 0

    def get_noisy_circuit(self) -> NoisyCircuit:
        self._num_noisy_operations = 0
        noisy_circuit = map_moments(circuit=self._circuit, map_func=self._get_noisy_moment, deep=True)
        return NoisyCircuit(
            circuit=noisy_circuit,
            num_noisy_operations=self._num_noisy_operations
        )

    def _get_noisy_moment(self, moment: Moment, moment_index: int) -> Sequence[Moment]:
        noisy_operations_on_active_qubits = [noisy_operation
                            for operation in moment.operations
                            for noisy_operation in self._get_noisy_operation(operation)]
        noisy_operations_on_inactive_qubits = [
            depolarize(p=self._noise_parameters.depolarization_probability_one_qubit).on(qubit)
            for qubit in self._get_all_qubits_in_circuit() - set(moment.qubits)
        ]
        noise_steps = Circuit(
            noisy_operations_on_active_qubits,
            noisy_operations_on_inactive_qubits
        )
        self._num_noisy_operations += len(list(noise_steps.all_operations()))
        return [moment, *noise_steps.moments]

    def _get_noisy_operation(self, operation: Operation) -> list[Operation]:
        if len(operation.qubits) > 2:
            return []
        noise_probability = self._noise_parameters.depolarization_probability_one_qubit \
            if len(operation.qubits) == 1 \
            else self._noise_parameters.depolarization_probability_two_qubit
        return [depolarize(p=noise_probability).on(qubit) for qubit in operation.qubits]

    def _get_all_qubits_in_circuit(self) -> set[Qid]:
        return set(self._circuit.all_qubits())

    @property
    def _noise_parameters(self) -> NoiseParameters:
        return ConfigurationErrorCorrectingCodeManager().get_configuration().noise_parameters
