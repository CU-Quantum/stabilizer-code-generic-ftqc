from enum import Enum, auto
from typing import Optional, Sequence

import numpy
from cirq import Circuit, CircuitOperation, I, Moment, OP_TREE, Operation, Qid, \
    TaggedOperation, X, Y, Z, map_moments

from cirq_experiments.custom_dataclasses.noise_parameters import NoiseParameters
from cirq_experiments.custom_dataclasses.noisy_circuit import NoisyCircuit
from cirq_experiments.custom_dataclasses.noisy_operations_count import NoisyOperationsCountPerCorrectionRound
from cirq_experiments.support.measurer.measurer import FAULT_TOLERANT_MEASURER_TAG
from cirq_experiments.support.operations_applier.operations_applier import DELAYED_NOISE_TAG
from cirq_experiments.globals.active_encodings_store import CORRECTION_ROUND_SYNDROMES_TAG
from cirq_experiments.globals.error_correcting_code_configuration import ConfigurationErrorCorrectingCodeManager

NOISY_CHANNEL_TAG = 'NoisyChannel'
NOISY_CHANNEL_ONE_QUBIT_TAG = 'NoisyChannel_OneQubit'
NOISY_CHANNEL_TWO_QUBIT_TAG = 'NoisyChannel_TwoQubit'


class NoisyChannelType(Enum):
    ONE = auto()
    TWO = auto()


# TODO each noisy moment can have either 1 or 2 qubit noise, not both (LINK1)
class NoisyCircuitCreator:
    def __init__(self, circuit: Circuit):
        self._circuit = circuit

    def get_noisy_circuit(self) -> NoisyCircuit:
        noisy_moments = map_moments(circuit=self._circuit,
                                    map_func=self._add_noisy_moment,
                                    deep=True,
                                    tags_to_ignore=[DELAYED_NOISE_TAG, FAULT_TOLERANT_MEASURER_TAG])  # FAULT_TOLERANT_MEASURER_TAG can cause infinite loop from nondeterminism
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
            self._get_depolarization_gate(noisy_channel_type=NoisyChannelType.ONE, qubit=qubit)
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
        if len(operation.qubits) > 2 or noise_was_added_recursively or FAULT_TOLERANT_MEASURER_TAG in operation.tags:
            return []

        noisy_channel_type = NoisyChannelType.ONE if len(operation.qubits) == 1 else NoisyChannelType.TWO
        return [self._get_depolarization_gate(noisy_channel_type=noisy_channel_type, qubit=qubit) for qubit in operation.qubits]

    def _get_delayed_noise(self, operation: Operation) -> list[Operation] | None:
        if DELAYED_NOISE_TAG in operation.tags:
            one_qubit, two_qubit = set(), set()
            for op in operation.sub_operation.circuit.all_operations():
                if len(op.qubits) == 1:
                    one_qubit.add(op.qubits[0])
                elif len(op.qubits) == 2:
                    two_qubit.add(op.qubits[0])
                    two_qubit.add(op.qubits[1])
            return [self._get_depolarization_gate(noisy_channel_type=NoisyChannelType.ONE, qubit=qubit) for qubit in one_qubit] \
                + [self._get_depolarization_gate(noisy_channel_type=NoisyChannelType.TWO, qubit=qubit) for qubit in two_qubit]
        return None

    def _count_noisy_ops_between_tags(self, op_tree: OP_TREE, path: Optional[list[int]] = None) -> NoisyOperationsCountPerCorrectionRound:
        if path is None:
            path = []
        path.append(-1)

        circuit = Circuit(op_tree)
        count = NoisyOperationsCountPerCorrectionRound()
        for i, op in enumerate(circuit.all_operations()):
            path[-1] = i
            if hasattr(op.untagged, 'circuit'):
                subcount = self._count_noisy_ops_between_tags(op_tree=op.untagged.circuit, path=path)
                count.add_count_to_latest(subcount.first_count)
                count.extend(subcount.tail)
            if CORRECTION_ROUND_SYNDROMES_TAG in op.tags:  # must come after recursion since errors during the measurement round would double up, causing incorrect syndrome
                count.append_correction_round()
            elif NOISY_CHANNEL_TAG in op.tags:
                if op.gate == X:
                    count.latest_count.x_errors.count += 1
                    count.latest_count.x_errors.paths.append(path.copy())
                elif op.gate == Y:
                    count.latest_count.y_errors.count += 1
                    count.latest_count.y_errors.paths.append(path.copy())
                elif op.gate == Z:
                    count.latest_count.z_errors.count += 1
                    count.latest_count.x_errors.paths.append(path.copy())
                else:
                    count.latest_count.i_errors.count += 1
                    count.latest_count.i_errors.paths.append(path.copy())

                if NOISY_CHANNEL_ONE_QUBIT_TAG in op.tags:
                    count.latest_count.one_qubit += 1
                elif NOISY_CHANNEL_TWO_QUBIT_TAG in op.tags:
                    count.latest_count.two_qubit += 1
        path.pop()
        return count

    def _get_depolarization_gate(self, noisy_channel_type: NoisyChannelType, qubit: Qid) -> Operation:
        probability = 0
        tag = ''
        if noisy_channel_type == NoisyChannelType.ONE:
            probability = self._noise_parameters.depolarization_probability_one_qubit
            tag = NOISY_CHANNEL_ONE_QUBIT_TAG
        elif noisy_channel_type == NoisyChannelType.TWO:
            probability = self._noise_parameters.depolarization_probability_two_qubit
            tag = NOISY_CHANNEL_TWO_QUBIT_TAG

        error_happens = numpy.random.random()
        error_gate = I
        if error_happens < probability:
            which_error = numpy.random.random()
            if which_error < 1 / 3:
                error_gate = X
            elif which_error < 2 / 3:
                error_gate = Y
            else:
                error_gate = Z
        return TaggedOperation(error_gate.on(qubit), NOISY_CHANNEL_TAG, tag)

    def _get_all_qubits_in_circuit(self) -> set[Qid]:
        return set(self._circuit.all_qubits())

    @property
    def _noise_parameters(self) -> NoiseParameters:
        return ConfigurationErrorCorrectingCodeManager().get_configuration().noise_parameters
