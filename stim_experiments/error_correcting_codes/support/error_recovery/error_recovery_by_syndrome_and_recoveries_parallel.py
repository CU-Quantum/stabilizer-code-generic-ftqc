from functools import reduce
from uuid import uuid4

from cirq import Circuit, FrozenCircuit, MeasurementKey, Operation
from sympy import And, Eq, symbols

from stim_experiments.custom_dataclasses.recovery import RecoveryOperation
from stim_experiments.error_correcting_codes.support.measurer.measurer import Measurer
from stim_experiments.globals.error_correcting_code_configuration import ConfigurationErrorCorrectingCodeManager


class ErrorRecoveryByStabilizersParallel:
    def __init__(self, stabilizers: list[list[Operation]], recoveries: list[RecoveryOperation]):
        self._stabilizers = stabilizers
        self._recoveries = recoveries

    def get_error_correction_circuit(self) -> Circuit:
        measurement_keys = [MeasurementKey(f'ERROR_RECOVERY_{uuid4().hex}') for _ in self._stabilizers]
        measurement_key_symbols = symbols([key.name for key in measurement_keys])

        sympy_equivalencies = [
            [Eq(key, val) for key, val in zip(measurement_key_symbols, recovery.symptom)]
            for recovery in self._recoveries
        ]
        recovery_operations = [
            recovery.operation.with_classical_controls(reduce(And, sympy_equivalence))
            for recovery, sympy_equivalence in zip(self._recoveries, sympy_equivalencies)
        ]

        syndrome_operations = self._measurer_type(
            observables=self._stabilizers,
            measurement_keys=measurement_keys,
        ).get_measurement_circuit()

        return Circuit(
            syndrome_operations,
            FrozenCircuit(recovery_operations),  # FrozenCircuit in order to ensure separate moment from syndrome extraction
        )

    @property
    def _measurer_type(self) -> type[Measurer]:
        return ConfigurationErrorCorrectingCodeManager().get_configuration().measurer_type
