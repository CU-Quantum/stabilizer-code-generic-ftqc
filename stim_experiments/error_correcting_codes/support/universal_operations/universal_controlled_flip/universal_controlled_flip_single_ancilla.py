from functools import cached_property
from uuid import uuid4

from cirq import Circuit, CircuitOperation, H, M, MeasurementKey, R

from stim_experiments.custom_dataclasses.logical_operation import LogicalGateLabel, LogicalOperation
from stim_experiments.error_correcting_codes.support.measurer.measurer import Measurer
from stim_experiments.error_correcting_codes.support.universal_operations.universal_controlled_flip.universal_controlled_flip import \
    UniversalControlledOperation
from stim_experiments.globals.error_correcting_code_configuration import ConfigurationErrorCorrectingCodeManager
from stim_experiments.globals.fresh_ancillas_pool import FreshAncillasPool


class UniversalControlledOperationSingleAncilla(UniversalControlledOperation):
    def get_controlled_operation_circuit(self) -> Circuit:
        logical_z_control = self._control.encoding.get_operation_circuit(LogicalOperation(gate=LogicalGateLabel.Z,
                                                                                          qubit_index=self._control.qubit_index_relative))
        with FreshAncillasPool().use_fresh_ancillas(num_ancillas=1) as ancilla_qubits:
            ancilla_qubit = ancilla_qubits[0]
            cz_ancilla_to_control = CircuitOperation(logical_z_control.freeze()).controlled_by(ancilla_qubit)
            c_operation_ancilla_to_target = CircuitOperation(
                self._target.encoding.get_operation_circuit(self._target.operation).freeze()
            ).controlled_by(ancilla_qubit)
            circuit = Circuit(
                H(ancilla_qubit),
                cz_ancilla_to_control,
                H(ancilla_qubit),
                c_operation_ancilla_to_target,
                H(ancilla_qubit),
                M(ancilla_qubit, key=self._measurement_key),
                CircuitOperation(logical_z_control.freeze()).with_classical_controls(self._measurement_key),
                R(ancilla_qubit),
            )
            return circuit

    @cached_property
    def _measurement_key(self) -> MeasurementKey:
        return MeasurementKey(f"UNIVERSAL_CONTROLLED_OPERATION_SINGLE_ANCILLA_{uuid4().hex}")
