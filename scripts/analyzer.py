from pathlib import Path

from cirq import Circuit, CircuitOperation, DEFAULT_RESOLVERS, FrozenCircuit, Moment, OP_TREE, Operation, \
    TaggedOperation, \
    read_json
from dacite import from_dict

from stim_experiments.custom_dataclasses.noisy_operations_count import NoisyOperationsCountPerCorrectionRound
from stim_experiments.serialization.custom_json_resolver import CustomJsonResolver
from stim_experiments.simulations.error_correcting_runner import ErrorCorrectingRunnerClifford


class Analyzer:
    def __init__(self, filepath: str, was_successful: callable):
        self._filepath = filepath
        self._was_successful = was_successful

    def analyze(self):
        with open(Path(self._housing_directory, 'errored_circuit_counts.json'), 'r') as f:
            errored_circuit_counts = from_dict(data_class=NoisyOperationsCountPerCorrectionRound, data=read_json(f))
        with open(Path(self._housing_directory, 'errored_circuit_operations.json'), 'r') as f:
            errored_circuit_operations = read_json(f, resolvers=[CustomJsonResolver()] + DEFAULT_RESOLVERS)

        for i, errored_circuit_operation in enumerate(errored_circuit_operations):
            circuit = errored_circuit_operation[0][0]
            moments_path = errored_circuit_operation[1]
            offending_operation = errored_circuit_operation[0][-1]
            circuit_without_operation = Circuit(
                self.remove_operation(moment=moment,
                                      moments_path=moments_path[1:],
                                      operation_to_remove=offending_operation)
                if i == moments_path[0] else moment
                for i, moment in enumerate(circuit)
            )
            results = ErrorCorrectingRunnerClifford().run_circuit(circuit_without_operation)
            success = self._was_successful(measurements_per_shot=results.measurements_per_shot)
            did_not_fail_when_error_was_removed = success
            if did_not_fail_when_error_was_removed:
                print(f"Noise at index {i} caused a failure.")
        a = 0

    def remove_operation(self, moment: Moment, moments_path: list[int], operation_to_remove: Operation) -> OP_TREE:
        if len(moment.operations) > 1: raise ValueError("Moment must have exactly one operation.")
        operation = moment.operations[0]
        circuit = operation.untagged.circuit.unfreeze()
        if len(moments_path) == 1:
            operations_to_remove = [(moments_path[0], operation_to_remove)]
            circuit.batch_remove(operations_to_remove)
            return TaggedOperation(
                CircuitOperation(circuit.freeze()),
                *operation.tags
            )
        else:
            return TaggedOperation(
                CircuitOperation(
                    FrozenCircuit(
                        self.remove_operation(
                            moment=moment,
                            moments_path=moments_path,
                            operation_to_remove=operation_to_remove)
                        if i == moments_path[0] else moment
                        for i, moment in enumerate(circuit)
                    )
                ),
                *operation.tags
            )

    @property
    def _housing_directory(self) -> Path:
        return Path(self._filepath).parent.resolve()
