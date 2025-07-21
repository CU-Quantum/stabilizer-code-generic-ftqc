from dataclasses import dataclass

from cirq import Circuit, Moment, Operation, Qid, depolarize

from stim_experiments.custom_dataclasses.noisy_moment import NoisyMoment


@dataclass
class NoiseParameters:
    depolarization_probability_one_qubit: float
    depolarization_probability_two_qubit: float

    def add_noisy_moment(self, moment: Moment, moment_index: int, inactive_qubits_all: set[Qid]) -> NoisyMoment:
        num_noisy_operations = 0
        inactive_qubits = inactive_qubits_all.copy()
        noise_ops: list[Operation] = []

        operations = moment.operations
        for operation in operations:
            if len(operation.qubits) > 2:
                continue
            noise_probability = self.depolarization_probability_one_qubit \
                if len(operation.qubits) == 1 \
                else self.depolarization_probability_two_qubit
            for qubit in operation.qubits:
                noise_ops.append(depolarize(p=noise_probability).on(qubit))
                inactive_qubits.discard(qubit)
                num_noisy_operations += 1

        noise_steps = Circuit(
            noise_ops,
            [
                depolarize(p=self.depolarization_probability_one_qubit).on(qubit)
                for qubit in inactive_qubits
            ]
        )

        return NoisyMoment(
            moments=[moment, *noise_steps.moments],
            num_noisy_operations=num_noisy_operations
        )
