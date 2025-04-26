from functools import cached_property

from cirq import Circuit, H, LineQubit, M, R

from stim_experiments.custom_dataclasses.logical_operation import LogicalGateLabel, LogicalOperation
from stim_experiments.error_correcting_codes.support.fault_tolerant_measurer.fault_tolerant_measurer import \
    FaultTolerantApplier, FaultTolerantMeasurer
from stim_experiments.error_correcting_codes.support.fault_tolerant_measurer.support.control_qubits_preparer import \
    StatePropagationParityEnsurer
from stim_experiments.simulators.simulator_using_circuits.custom_dataclasses.simulation_operation import \
    SimulationOperation


class CircuitFromOperationCreator:
    def __init__(self, operation: SimulationOperation, ancilla_qubits: list[LineQubit], num_state_qubits: int):
        self._operation = operation
        self._encoding_ancilla_qubits = ancilla_qubits
        self._num_state_qubits = num_state_qubits

    def create_circuit(self) -> Circuit:
        if self._operation.target_encoding:
            return self._get_controlled_circuit() if self._operation.control_encoding else self._logical_operation_on_target
        elif self._operation.control_encoding:
            return self._get_measurement_circuit()
        else:
            raise ValueError('Was given a SimulationOperation with no encoding.')

    def _get_controlled_circuit(self) -> Circuit:
        target_operations = list(self._logical_operation_on_target.all_operations())
        control_operations = list(self._logical_z_on_control.all_operations())
        num_target_operations = len(target_operations)
        # ancillas_needed = max(num_target_operations, len(control_operations))
        # ancillas = self._encoding_ancilla_qubits + LineQubit.range(self._num_state_qubits, self._num_state_qubits + ancillas_needed)

        controls_needed = num_target_operations
        control_measurements = LineQubit.range(self._num_state_qubits, self._num_state_qubits + controls_needed)
        control_ancillas = self._encoding_ancilla_qubits + LineQubit.range(control_measurements[-1].x, control_measurements[-1].x + len(control_operations))
        control_propagator = [
            FaultTolerantApplier(
                operations=control_operations,
                measurement_qubit=control_measurements[i],
                ancillas=control_ancillas,
                measurement_qubit_preparer=Circuit(H(control_measurements[i])),
            ).get_circuit()
            for i in range(controls_needed)
        ]
        target_controlled_by_ancilla = [target_operation.controlled_by(control_measurement)
                                        for target_operation, control_measurement in zip(target_operations, control_measurements)]
        return Circuit(
            control_propagator,
            target_controlled_by_ancilla,
            [R(qubit) for qubit in control_measurements + control_ancillas]
        )

    def _get_measurement_circuit(self) -> Circuit:
        measurement_qubit = self._encoding_ancilla_qubits[0]
        hadamard_first_qubit = Circuit(H(measurement_qubit))
        applier = FaultTolerantApplier(operations=list(self._logical_z_on_control.all_operations()),
                                       measurement_qubit=measurement_qubit,
                                       ancillas=self._encoding_ancilla_qubits[1:],
                                       measurement_qubit_preparer=hadamard_first_qubit,
                                       measurement_key=str(self._operation.control_encoding.qubit_index_logical),
                                       )
        return Circuit(
            applier.get_circuit(),
            R(measurement_qubit),
        )

    @cached_property
    def _logical_z_on_control(self) -> Circuit:
        control_operation = LogicalOperation(
            gate=LogicalGateLabel.Z,
            qubit_index=self._operation.control_encoding.qubit_index_relative
        )
        return self._operation.control_encoding.encoding.get_operation_circuit(operation=control_operation)

    @cached_property
    def _logical_operation_on_target(self) -> Circuit:
        return self._operation.target_encoding.encoding.get_operation_circuit(operation=self._operation.target_encoding.operation)
