from functools import cached_property

from cirq import Circuit, H, LineQubit, M, R

from stim_experiments.custom_dataclasses.logical_operation import LogicalGateLabel, LogicalOperation
from stim_experiments.simulators.simulator_using_circuits.custom_dataclasses.simulation_operation import \
    SimulationOperation


class CircuitFromOperationCreator:
    def __init__(self, operation: SimulationOperation, control_ancilla: LineQubit):
        self._operation = operation
        self._ancilla_qubit = control_ancilla

    def create_circuit(self) -> Circuit:
        if self._operation.target_encoding:
            return self._get_controlled_circuit() if self._operation.control_encoding else self._target_circuit
        elif self._operation.control_encoding:
            return self._get_measurement_circuit()
        else:
            raise ValueError('Was given a SimulationOperation with no encoding.')

    def _get_controlled_circuit(self) -> Circuit:
        target_controlled_by_ancilla = [operation.controlled_by(self._ancilla_qubit) for operation in
                                        self._target_circuit.all_operations()]
        return Circuit(
            self._control_controlled_by_ancilla,
            target_controlled_by_ancilla,
            self._control_controlled_by_ancilla,
        )

    def _get_measurement_circuit(self) -> Circuit:
        return Circuit(
            self._control_controlled_by_ancilla,
            M(self._ancilla_qubit),
            R(self._ancilla_qubit),
        )

    @cached_property
    def _control_controlled_by_ancilla(self) -> Circuit:
        control_controlled_by_ancilla = [operation.controlled_by(self._ancilla_qubit) for operation in
                                         self._control_circuit.all_operations()]
        return Circuit(
            H(self._ancilla_qubit),
            control_controlled_by_ancilla,
            H(self._ancilla_qubit),
        )

    @cached_property
    def _control_circuit(self) -> Circuit:
        control_operation = LogicalOperation(
            gate=LogicalGateLabel.Z,
            qubit_index=self._operation.control_encoding.qubit_index
        )
        return self._operation.control_encoding.encoding.get_operation_circuit(operation=control_operation)

    @cached_property
    def _target_circuit(self) -> Circuit:
        return self._operation.target_encoding.encoding.get_operation_circuit(
            operation=self._operation.target_encoding.operation)
