from functools import cached_property

from cirq import Circuit, MeasurementKey

from stim_experiments.custom_dataclasses.logical_operation import LogicalGateLabel, LogicalOperation
from stim_experiments.custom_dataclasses.simulation_operation import \
    SimulationOperation
from stim_experiments.error_correcting_codes.support.measurer.measurer import Measurer
from stim_experiments.error_correcting_codes.support.universal_operations.universal_controlled_operation.universal_controlled_operation import \
    UniversalControlledOperation
from stim_experiments.error_correcting_codes.support.universal_operations.universal_hadamard.universal_hadamard import UniversalHadamard
from stim_experiments.globals.error_correcting_code_configuration import ConfigurationErrorCorrectingCodeManager
from stim_experiments.custom_dataclasses.configuration_error_correcing_code import ConfigurationErrorCorrectingCode
from stim_experiments.utilities.universal_controlled_operation_type_factory import \
    UniversalControlledOperationTypeFactory
from stim_experiments.utilities.universal_hadamard_type_factory import UniversalHadamardTypeFactory


class CircuitFromOperationCreator:
    def __init__(self, operation: SimulationOperation, num_state_qubits: int):
        self._operation = operation
        self._num_state_qubits = num_state_qubits

    def create_circuit(self) -> Circuit:
        if self._operation.target_encoding:
            return self._get_controlled_circuit() if self._operation.control_encoding else self._logical_operation_on_target
        elif self._operation.control_encoding:
            return self._get_measurement_circuit()
        else:
            raise ValueError('Was given a SimulationOperation with no encoding.')

    def _get_controlled_circuit(self) -> Circuit:
        return self._universal_controlled_operation_type(control=self._operation.control_encoding,
                                                         target=self._operation.target_encoding
                                                         ).get_controlled_operation_circuit()

    def _get_measurement_circuit(self) -> Circuit:
        measurer = self._measurer_type(
            operations=list(self._logical_z_on_control.all_operations()),
            measurement_key=MeasurementKey(str(self._operation.control_encoding.qubit_index_logical)),
        )
        return measurer.get_measurement_circuit()

    @cached_property
    def _logical_z_on_control(self) -> Circuit:
        control_operation = LogicalOperation(
            gate=LogicalGateLabel.Z,
            qubit_index=self._operation.control_encoding.qubit_index_relative
        )
        return self._operation.control_encoding.encoding.get_operation_circuit(operation=control_operation)

    @cached_property
    def _logical_operation_on_target(self) -> Circuit:
        operations = self._operation.target_encoding.encoding.get_operation_circuit(operation=self._operation.target_encoding.operation)
        if operations is None and self._operation.target_encoding.operation.gate == LogicalGateLabel.H:
            target_index = self._operation.target_encoding.operation.qubit_index
            return self._universal_hadamard_type(  # TODO test this
                code=self._operation.target_encoding.encoding,
                qubit_index=target_index
            ).get_hadamard_circuit()
        return operations

    @property
    def _measurer_type(self) -> type[Measurer]:
        return self._configuration.measurer_type

    @property
    def _universal_controlled_operation_type(self) -> type[UniversalControlledOperation]:
        return UniversalControlledOperationTypeFactory(self._configuration.universal_controlled_operation_type).get_universal_controlled_operation_type()

    @property
    def _universal_hadamard_type(self) -> type[UniversalHadamard]:
        return UniversalHadamardTypeFactory(self._configuration.universal_hadamard_type).get_universal_hadamard_type()

    @property
    def _configuration(self) -> ConfigurationErrorCorrectingCode:
        return ConfigurationErrorCorrectingCodeManager().get_configuration()
