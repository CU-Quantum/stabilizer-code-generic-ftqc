from collections import defaultdict
from typing import Sequence

from cirq import Circuit, CircuitOperation, LineQubit, Moment, Operation, Qid, ResetChannel, depolarize, map_moments

from stim_experiments.custom_dataclasses.noise_parameters import NoiseParameters
from stim_experiments.custom_dataclasses.noisy_circuit import NoisyCircuit
from stim_experiments.error_correcting_codes.support.measurer.fault_tolerant_measurer.fault_tolerant_measurer import \
    FAULT_TOLERANT_MEASURER_TAG
from stim_experiments.globals.error_correcting_code_configuration import ConfigurationErrorCorrectingCodeManager


# TODO during fault tolerant measurement, only insert noise on data qubits after all measurements
class NoisyCircuitCreator:
    def __init__(self, circuit: Circuit, num_data_qubits: int):
        self._circuit = circuit
        self._num_data_qubits = num_data_qubits
        self._num_noisy_operations = 0
        self._measurement_operation = defaultdict(set)

    def get_noisy_circuit(self) -> NoisyCircuit:
        self._num_noisy_operations = 0
        ancilla_qubits = self._get_all_qubits_in_circuit() - set(LineQubit.range(self._num_data_qubits))
        noisy_moments = map_moments(circuit=self._circuit, map_func=self._add_noisy_moment, deep=True)
        return NoisyCircuit(
            circuit=Circuit(
                noisy_moments,
                ResetChannel().on_each(*ancilla_qubits)
            ),
            num_noisy_operations=self._num_noisy_operations
        )

    def _add_noisy_moment(self, moment: Moment, moment_index: int) -> Sequence[Moment]:
        # circuit = Circuit(moment)
        # qubits_with_one_qubit_gate = {qubit
        #                               for op in circuit.findall_operations(lambda op: len(op.qubits) == 1)
        #                               for qubit in op[1].qubits}
        # qubits_with_two_qubit_gate = {qubit
        #                               for op in circuit.findall_operations(lambda op: len(op.qubits) == 2)
        #                               for qubit in op[1].qubits}
        #
        # noisy_operations_on_active_qubits = \
        #     [depolarize(p=self._noise_parameters.depolarization_probability_one_qubit).on(qubit)
        #      for qubit in qubits_with_one_qubit_gate] \
        #     + [depolarize(p=self._noise_parameters.depolarization_probability_two_qubit).on(qubit)
        #                          for qubit in qubits_with_two_qubit_gate]
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
        # if FAULT_TOLERANT_MEASURER_TAG in operation.tags:
        #     circuit_operation: CircuitOperation = operation.untagged
        #     circuit = circuit_operation.circuit
        #     reset_qubits = {qubit
        #                     for op in circuit.findall_operations_with_gate_type(ResetChannel)
        #                     for qubit in op[1].qubits}
        #     qubits_with_one_qubit_gate = {qubit
        #                                   for op in circuit.findall_operations(lambda op: len(op.qubits) == 1)
        #                                   for qubit in op[1].qubits}
        #     qubits_with_two_qubit_gate = {qubit
        #                                   for op in circuit.findall_operations(lambda op: len(op.qubits) == 2)
        #                                   for qubit in op[1].qubits}
        #     self._measurement_operation['ancilla_qubits'].update(reset_qubits)
        #     self._measurement_operation['one'].update(set(qubits_with_one_qubit_gate))
        #     self._measurement_operation['two'].update(set(qubits_with_two_qubit_gate))
        #     return []
        # elif len(self._measurement_operation):
        #     self._measurement_operation = defaultdict(set)
        #     return [depolarize(p=self._noise_parameters.depolarization_probability_one_qubit).on(qubit)
        #             for qubit in self._measurement_operation['one'] - self._measurement_operation['ancilla_qubits']] \
        #         + [depolarize(p=self._noise_parameters.depolarization_probability_two_qubit).on(qubit)
        #             for qubit in self._measurement_operation['two'] - self._measurement_operation['ancilla_qubits']]

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
