from functools import cached_property
from uuid import uuid4

import sympy
from cirq import Circuit, H, M, MeasurementKey, R

from stim_experiments.custom_dataclasses.logical_operation import LogicalGateLabel, LogicalOperation
from stim_experiments.error_correcting_codes.support.measurer.measurer import Measurer
from stim_experiments.error_correcting_codes.support.universal_operations.universal_hadamard.universal_hadamard import UniversalHadamard
from stim_experiments.globals.error_correcting_code_configuration import ConfigurationErrorCorrectingCodeManager
from stim_experiments.globals.fresh_ancillas_pool import FreshAncillasPool


class UniversalHadamardSingleAncilla(UniversalHadamard):
    def get_hadamard_circuit(self):
        logical_x, logical_z = logical_operations = [
            self._code.get_operation_circuit(LogicalOperation(gate=label, qubit_index=self._qubit_index))
            for label in (LogicalGateLabel.X, LogicalGateLabel.Z)
        ]
        with FreshAncillasPool().use_fresh_ancillas(num_ancillas=1) as ancilla_qubits:
            ancilla_qubit = ancilla_qubits[0]
            logical_cx, logical_cz = (
                [
                    op.controlled_by(ancilla_qubit)
                    for op in logical_operation.all_operations()
                ]
                for logical_operation in logical_operations
            )
            circuit = Circuit(
                H(ancilla_qubit),
                logical_cx,
                logical_cz,
                H(ancilla_qubit),
                M(ancilla_qubit, key=self._measurement_key),
                [
                    op.with_classical_controls(self._measurement_key)
                    for op in logical_x.all_operations()
                ],
                [
                    op.with_classical_controls(sympy.Eq(self._measurement_key_symbol, 0))
                    for op in logical_z.all_operations()
                ],
                R(ancilla_qubit),
            )
            return circuit

    @cached_property
    def _measurement_key_symbol(self) -> MeasurementKey:
        return sympy.symbols(self._measurement_key.name)

    @cached_property
    def _measurement_key(self) -> MeasurementKey:
        return MeasurementKey(f"UNIVERSAL_HADAMARD_SINGLE_ANCILLA_{uuid4().hex}")

    @property
    def _measurer_type(self) -> type[Measurer]:
        configuration = ConfigurationErrorCorrectingCodeManager().get_configuration()
        return configuration.measurer_type
