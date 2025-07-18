from uuid import uuid4

from cirq import Circuit, CircuitOperation, FrozenCircuit, LineQubit, MeasurementKey, Operation

from stim_experiments.custom_dataclasses.check_matrix import CheckMatrix
from stim_experiments.error_correcting_codes.support.check_matrix_to_operations import CheckMatrixToOperations
from stim_experiments.error_correcting_codes.support.measurer.measurer import Measurer
from stim_experiments.error_correcting_codes.support.state_encoder.state_encoder import StateEncoder
from stim_experiments.globals.error_correcting_code_configuration import ConfigurationErrorCorrectingCodeManager


class StateEncoderByGeneratorMeasurement(StateEncoder):
    def __init__(self,
                 check_matrix: CheckMatrix,
                 phase_corrections: list[list[Operation]],
                 qubits: list[LineQubit],
                 ):
        self._check_matrix = check_matrix
        self._phase_corrections = phase_corrections
        self._qubits = qubits

    def encode_state(self) -> Circuit:
        measurement_keys = [MeasurementKey(f'STATE_ENCODER_{i}_{uuid4()}') for i in range(len(self._check_matrix.matrix))]
        generators = CheckMatrixToOperations(check_matrix=self._check_matrix, qubits=self._qubits).get_operations()
        return Circuit(
            [
                [
                    self._measurer_type(operations=[operation for target_index, operation in enumerate(operations)],
                                        measurement_key=measurement_key).get_measurement_circuit(),
                    [
                        phase_correction.with_classical_controls(measurement_key)
                        for phase_correction in self._phase_corrections[generator_index]
                    ],
                ]
                for generator_index, (measurement_key, operations) in enumerate(zip(measurement_keys, generators))
            ],
        )

    @property
    def _measurer_type(self) -> type[Measurer]:
        configuration = ConfigurationErrorCorrectingCodeManager().get_configuration()
        return configuration.measurer_type
