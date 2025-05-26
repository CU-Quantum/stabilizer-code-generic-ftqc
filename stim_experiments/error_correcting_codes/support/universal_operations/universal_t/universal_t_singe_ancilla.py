from functools import cached_property
from uuid import uuid4

from cirq import Circuit, CircuitOperation, H, M, MeasurementKey, R, T

from stim_experiments.custom_dataclasses.logical_operation import LogicalGateLabel, LogicalOperation
from stim_experiments.error_correcting_codes.support.universal_operations.universal_t.universal_t import UniversalT
from stim_experiments.globals.fresh_ancillas_pool import FreshAncillasPool


class UniversalTSingleAncilla(UniversalT):
    def get_t_circuit(self) -> Circuit:
        logical_z_control = self._encoding.encoding.get_operation_circuit(LogicalOperation(gate=LogicalGateLabel.Z, qubit_index=self._encoding.qubit_index_relative))
        with FreshAncillasPool().use_fresh_ancillas(num_ancillas=1) as ancilla_qubits:
            ancilla_qubit = ancilla_qubits[0]
            cz_ancilla_to_control = CircuitOperation(logical_z_control.freeze()).controlled_by(ancilla_qubit)
            return Circuit(
                H(ancilla_qubit),
                cz_ancilla_to_control,
                H(ancilla_qubit),
                T(ancilla_qubit),
                H(ancilla_qubit),
                M(ancilla_qubit, key=self._measurement_key),
                CircuitOperation(logical_z_control.freeze()).with_classical_controls(self._measurement_key),
                R(ancilla_qubit),
            )

    @cached_property
    def _measurement_key(self) -> MeasurementKey:
        return MeasurementKey(f"UNIVERSAL_T_SINGLE_ANCILLA_{uuid4().hex}")
