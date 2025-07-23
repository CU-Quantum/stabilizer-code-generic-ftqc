from typing import Sequence

from cirq import Circuit, CircuitOperation, LineQubit, Moment, Operation, Qid, ResetChannel, \
    depolarize, map_moments

from stim_experiments.custom_dataclasses.noise_parameters import NoiseParameters
from stim_experiments.custom_dataclasses.noisy_circuit import NoisyCircuit
from stim_experiments.custom_dataclasses.noisy_operations_count import NoisyOperationsCount
from stim_experiments.error_correcting_codes.support.operations_applier.operations_applier import DELAYED_NOISE_TAG
from stim_experiments.globals.error_correcting_code_configuration import ConfigurationErrorCorrectingCodeManager


class NoisyCircuitCreator:
    def __init__(self, circuit: Circuit, num_data_qubits: int):
        self._circuit = circuit
        self._num_data_qubits = num_data_qubits
        self._noisy_operations_count = NoisyOperationsCount()

    def get_noisy_circuit(self) -> NoisyCircuit:
        self._noisy_operations_count = NoisyOperationsCount()
        ancilla_qubits = self._get_all_qubits_in_circuit() - set(LineQubit.range(self._num_data_qubits))
        noisy_moments = map_moments(circuit=self._circuit,
                                    map_func=self._add_noisy_moment,
                                    deep=True,
                                    tags_to_ignore=[DELAYED_NOISE_TAG])
        return NoisyCircuit(
            circuit=Circuit(
                noisy_moments,
                ResetChannel().on_each(*ancilla_qubits)
            ),
            noisy_operations_count=self._noisy_operations_count
        )

    def _add_noisy_moment(self, moment: Moment, moment_index: int) -> Sequence[Moment]:
        noisy_operations_on_active_qubits = [noisy_operation
                                             for operation in moment.operations
                                             for noisy_operation in self._get_noisy_operation(operation)]
        noisy_operations_on_inactive_qubits = [
            depolarize(p=self._noise_parameters.depolarization_probability_one_qubit).on(qubit)
            for qubit in self._get_all_qubits_in_circuit() - set(moment.qubits)
        ]
        self._noisy_operations_count.one_qubit += len(noisy_operations_on_inactive_qubits)
        noise_steps = Circuit(
            noisy_operations_on_active_qubits,
            noisy_operations_on_inactive_qubits
        )
        return [moment, *noise_steps.moments]

    def _get_noisy_operation(self, operation: Operation) -> list[Operation]:
        delayed_noise = self._get_delayed_noise(operation=operation)
        if delayed_noise is not None:
            return delayed_noise

        noise_was_added_recursively = isinstance(operation.untagged, CircuitOperation)
        if len(operation.qubits) > 2 or noise_was_added_recursively:
            return []

        if len(operation.qubits) == 1:
            noise_probability = self._noise_parameters.depolarization_probability_one_qubit
            self._noisy_operations_count.one_qubit += len(operation.qubits)
        else:
            noise_probability = self._noise_parameters.depolarization_probability_two_qubit
            self._noisy_operations_count.two_qubit += len(operation.qubits)
        return [depolarize(p=noise_probability).on(qubit) for qubit in operation.qubits]

    def _get_delayed_noise(self, operation: Operation) -> list[Operation] | None:
        if DELAYED_NOISE_TAG in operation.tags:
            one_qubit, two_qubit = set(), set()
            for op in operation.sub_operation.circuit.all_operations():
                if len(op.qubits) == 1:
                    one_qubit.add(op.qubits[0])
                elif len(op.qubits) == 2:
                    two_qubit.add(op.qubits[0])
                    two_qubit.add(op.qubits[1])
            self._noisy_operations_count.one_qubit += len(one_qubit)
            self._noisy_operations_count.two_qubit += len(two_qubit)
            return depolarize(p=self._noise_parameters.depolarization_probability_one_qubit).on_each(*one_qubit) \
                + depolarize(p=self._noise_parameters.depolarization_probability_two_qubit).on_each(*two_qubit)
        return None

    def _get_all_qubits_in_circuit(self) -> set[Qid]:
        return set(self._circuit.all_qubits())

    @property
    def _noise_parameters(self) -> NoiseParameters:
        return ConfigurationErrorCorrectingCodeManager().get_configuration().noise_parameters
