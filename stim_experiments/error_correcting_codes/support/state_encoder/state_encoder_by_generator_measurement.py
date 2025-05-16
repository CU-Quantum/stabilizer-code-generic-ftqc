from uuid import uuid4

from cirq import Circuit, CircuitOperation, FrozenCircuit, MeasurementKey, Operation

from stim_experiments.globals.error_correcting_code_configuration import ConfigurationErrorCorrectingCodeManager


class StateEncoderByGeneratorMeasurement:
    def __init__(self, generators: list[list[Operation]], phase_corrections: list[list[Operation]]):
        self._generators = generators
        self._phase_corrections = phase_corrections

        configuration = ConfigurationErrorCorrectingCodeManager().get_configuration()
        self._measurer_type = configuration.measurer_type

    def encode_state(self) -> Circuit:
        measurement_keys = [MeasurementKey(f'STATE_ENCODER_{i}_{uuid4()}') for i in range(len(self._generators))]
        return Circuit(
            [
                [
                    self._measurer_type(operations=[operation for target_index, operation in enumerate(operations)],
                                        measurement_key=measurement_key).get_measurement_circuit(),
                    CircuitOperation(
                        FrozenCircuit(self._phase_corrections[generator_index]),
                    ).with_classical_controls(measurement_key),
                ]
                for generator_index, (measurement_key, operations) in enumerate(zip(measurement_keys, self._generators))
            ],
        )
