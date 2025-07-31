from functools import cached_property
from uuid import uuid4

from cirq import Circuit, H, M, MeasurementKey, R

from stim_experiments.custom_dataclasses.logical_operation import LogicalGateLabel, LogicalOperation
from stim_experiments.error_correcting_codes.support.universal_operations.universal_controlled_flip.universal_controlled_flip import \
    UniversalControlledOperation
from stim_experiments.globals.fresh_ancillas_pool import FreshAncillasPool


class UniversalControlledOperationSingleAncilla(UniversalControlledOperation):
    def get_controlled_operation_circuit(self) -> Circuit:
        logical_z_control = self._control.encoding.get_operation_circuit(LogicalOperation(gate=LogicalGateLabel.Z,
                                                                                          qubit_index=self._control.qubit_index_relative))
        with FreshAncillasPool().use_fresh_ancillas(num_ancillas=1) as ancilla_qubits:
            ancilla_qubit = ancilla_qubits[0]
            cz_ancilla_to_control = [
                op.controlled_by(ancilla_qubit)
                for op in logical_z_control.all_operations()
            ]
            c_operation_ancilla_to_target = [
                op.controlled_by(ancilla_qubit)
                for op in self._target.encoding.get_operation_circuit(self._target.operation).all_operations()
            ]
            circuit = Circuit(
                R(ancilla_qubit),
                H(ancilla_qubit),
                cz_ancilla_to_control,
                H(ancilla_qubit),
                c_operation_ancilla_to_target,
                H(ancilla_qubit),
                M(ancilla_qubit, key=self._measurement_key),
                [
                    op.with_classical_controls(self._measurement_key)
                    for op in logical_z_control.all_operations()
                ],
            )
            return circuit

    @cached_property
    def _measurement_key(self) -> MeasurementKey:
        return MeasurementKey(f"UNIVERSAL_CONTROLLED_OPERATION_SINGLE_ANCILLA_{uuid4().hex}")
