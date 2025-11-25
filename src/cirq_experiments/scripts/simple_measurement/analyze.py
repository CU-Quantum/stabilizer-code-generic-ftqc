from cirq import DEFAULT_RESOLVERS, read_json
from dacite import from_dict

from cirq_experiments.custom_dataclasses.noisy_operations_count import NoisyOperationsCountPerCorrectionRound
from cirq_experiments.serialization.custom_json_resolver import CustomJsonResolver

if __name__ == '__main__':
    with open('errored_circuit_counts.json', 'r') as f:
        errored_circuit_counts = from_dict(data_class=NoisyOperationsCountPerCorrectionRound, data=read_json(f))
    with open('errored_circuit_operations.json', 'r') as f:
        errored_circuit_operations = read_json(f, resolvers=[CustomJsonResolver()] + DEFAULT_RESOLVERS)
    a = 0
