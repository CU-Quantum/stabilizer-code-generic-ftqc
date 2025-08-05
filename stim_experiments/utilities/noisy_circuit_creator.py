from abc import ABC
from enum import Enum, auto
from typing import Sequence

import numpy
from cirq import Circuit, CircuitOperation, Gate, I, Moment, OP_TREE, Operation, Qid, \
    X, Y, map_moments, unitary

from stim_experiments.custom_dataclasses.noise_parameters import NoiseParameters
from stim_experiments.custom_dataclasses.noisy_circuit import NoisyCircuit
from stim_experiments.custom_dataclasses.noisy_operations_count import NoisyOperationsCountPerShot, NoisyOperationsCountPerCorrectionRound
from stim_experiments.error_correcting_codes.support.operations_applier.operations_applier import DELAYED_NOISE_TAG
from stim_experiments.globals.active_encodings_store import CORRECTION_ROUND_TAG
from stim_experiments.globals.error_correcting_code_configuration import ConfigurationErrorCorrectingCodeManager


class NoisyChannelType(Enum):
    ONE = auto()
    TWO = auto()


class NoisyChannel(Gate, ABC):
    def __init__(self, noisy_channel_type: NoisyChannelType):
        self.noisy_channel_type = noisy_channel_type
        self._noisy_operations_count = NoisyOperationsCountPerShot()

    def set_noisy_operations_count(self, noisy_operations_count: NoisyOperationsCountPerShot) -> None:
        self._noisy_operations_count = noisy_operations_count


class NoisyChannelDepolarizing(NoisyChannel):
    def __init__(self, noisy_channel_type: NoisyChannelType, probability: float):
        super().__init__(noisy_channel_type=noisy_channel_type)
        self._probability = probability

    def _unitary_(self):
        error_happens = numpy.random.random()
        error_gate = I
        if error_happens < self._probability:
            which_error = numpy.random.random()
            if which_error < 1 / 3:
                self._noisy_operations_count.x_errors += 1
                error_gate = X
            elif which_error < 2 / 3:
                self._noisy_operations_count.y_errors += 1
                error_gate = Y
            else:
                self._noisy_operations_count.z_errors += 1
        return unitary(error_gate)

    def _num_qubits_(self) -> int:
        return 1


class NoisyCircuitCreator:
    def __init__(self, circuit: Circuit, num_data_qubits: int):
        self._circuit = circuit
        self._num_data_qubits = num_data_qubits

    def get_noisy_circuit(self) -> NoisyCircuit:
        noisy_moments = map_moments(circuit=self._circuit,
                                    map_func=self._add_noisy_moment,
                                    deep=True,
                                    tags_to_ignore=[DELAYED_NOISE_TAG])
        noisy_operations_count = self._count_noisy_ops_between_tags(op_tree=noisy_moments)
        return NoisyCircuit(
            circuit=noisy_moments,
            noisy_operations_count=noisy_operations_count
        )

    def _add_noisy_moment(self, moment: Moment, moment_index: int) -> Sequence[Moment]:
        noisy_operations_on_active_qubits = [noisy_operation
                                             for operation in moment.operations
                                             for noisy_operation in self._get_noisy_operation(operation)]
        noisy_operations_on_inactive_qubits = [
            self._get_depolarization_gate(noisy_channel_type=NoisyChannelType.ONE).on(qubit)
            for qubit in self._get_all_qubits_in_circuit() - set(moment.qubits)
        ]
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

        noisy_channel_type = NoisyChannelType.ONE if len(operation.qubits) == 1 else NoisyChannelType.TWO
        return [self._get_depolarization_gate(noisy_channel_type=noisy_channel_type).on(qubit) for qubit in operation.qubits]

    def _get_delayed_noise(self, operation: Operation) -> list[Operation] | None:
        if DELAYED_NOISE_TAG in operation.tags:
            one_qubit, two_qubit = set(), set()
            for op in operation.sub_operation.circuit.all_operations():
                if len(op.qubits) == 1:
                    one_qubit.add(op.qubits[0])
                elif len(op.qubits) == 2:
                    two_qubit.add(op.qubits[0])
                    two_qubit.add(op.qubits[1])
            return self._get_depolarization_gate(noisy_channel_type=NoisyChannelType.ONE).on_each(*one_qubit) \
                + self._get_depolarization_gate(noisy_channel_type=NoisyChannelType.TWO).on_each(*two_qubit)
        return None

    def _count_noisy_ops_between_tags(self, op_tree: OP_TREE) -> NoisyOperationsCountPerCorrectionRound:
        circuit = Circuit(op_tree)
        count = NoisyOperationsCountPerCorrectionRound()
        for op in circuit.all_operations():
            if hasattr(op.untagged, 'circuit'):
                subcount = self._count_noisy_ops_between_tags(op_tree=op.untagged.circuit)
                count.add_count_to_latest(subcount.first_count)
                count.extend(subcount.tail)
            if CORRECTION_ROUND_TAG in op.tags:
                count.append_correction_round()
            elif isinstance(op.gate, NoisyChannel):
                gate_with_type: NoisyChannel = op.gate
                gate_with_type.set_noisy_operations_count(count.latest_count)
                if gate_with_type.noisy_channel_type == NoisyChannelType.ONE:
                    count.latest_count.one_qubit += 1
                elif gate_with_type.noisy_channel_type == NoisyChannelType.TWO:
                    count.latest_count.two_qubit += 1
        return count

    def _get_depolarization_gate(self, noisy_channel_type: NoisyChannelType) -> Gate:
        probability = 0
        if noisy_channel_type == NoisyChannelType.ONE:
            probability = self._noise_parameters.depolarization_probability_one_qubit
        elif noisy_channel_type == NoisyChannelType.TWO:
            probability = self._noise_parameters.depolarization_probability_two_qubit
        return NoisyChannelDepolarizing(noisy_channel_type=noisy_channel_type, probability=probability)

    def _get_all_qubits_in_circuit(self) -> set[Qid]:
        return set(self._circuit.all_qubits())

    @property
    def _noise_parameters(self) -> NoiseParameters:
        return ConfigurationErrorCorrectingCodeManager().get_configuration().noise_parameters
