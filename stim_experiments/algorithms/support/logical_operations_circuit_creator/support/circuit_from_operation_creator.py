from functools import cached_property

from cirq import Circuit, CircuitOperation, FrozenCircuit, MeasurementKey

from stim_experiments.conditions.majority_vote import MajorityVote
from stim_experiments.custom_dataclasses.logical_operation import LogicalGateLabel, LogicalOperation
from stim_experiments.custom_dataclasses.simulation_operation import \
    LogicalEncodingIndex, SimulationOperation
from stim_experiments.error_correcting_codes.support.measurer.measurer import Measurer
from stim_experiments.error_correcting_codes.support.universal_operations.universal_controlled_flip.universal_controlled_flip import \
    UniversalControlledOperation
from stim_experiments.error_correcting_codes.support.universal_operations.universal_hadamard.universal_hadamard import UniversalHadamard
from stim_experiments.error_correcting_codes.support.universal_operations.universal_t.universal_t import UniversalT
from stim_experiments.globals.active_encodings_store import ActiveEncodingsStore
from stim_experiments.globals.error_correcting_code_configuration import ConfigurationErrorCorrectingCodeManager
from stim_experiments.custom_dataclasses.configuration_error_correcing_code import ConfigurationErrorCorrectingCode


class CircuitFromOperationCreator:
    def __init__(self, operation: SimulationOperation):
        self._operation = operation

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
        control_operation = LogicalOperation(
            gate=LogicalGateLabel.Z,
            qubit_index=self._operation.control_encoding.qubit_index_relative
        )
        logical_z_on_control = self._operation.control_encoding.encoding.get_operation_circuit(operation=control_operation)
        majority_vote = MajorityVote(desired_measurement_key=MeasurementKey(str(self._operation.control_encoding.qubit_index_logical)))
        measurer = self._measurer_type(
            observables=[list(logical_z_on_control.all_operations())],
            measurement_keys=[majority_vote.key],
        )
        with ActiveEncodingsStore(additional_tracked_encodings=[]) as encodings_store:
            subcircuit = FrozenCircuit(
                measurer.get_measurement_circuit(),
                encodings_store.get_all_correction_circuits()
            )
            circuit_operation = self._get_hacked_circuit_operation(subcircuit=subcircuit, majority_vote=majority_vote)
            return Circuit(circuit_operation)

    def _get_hacked_circuit_operation(self, subcircuit: FrozenCircuit, majority_vote: MajorityVote) -> CircuitOperation:
        self._hack_to_add_desired_key_to_list_of_modified_keys(subcircuit, majority_vote)
        circuit_operation = CircuitOperation(
            subcircuit,
            use_repetition_ids=False,
            repeat_until=majority_vote
        )
        replace = circuit_operation.replace

        def _replace(**changes) -> CircuitOperation:
            subcircuit = changes['circuit']
            self._hack_to_add_desired_key_to_list_of_modified_keys(subcircuit, majority_vote)
            return replace(**changes)

        circuit_operation.replace = _replace
        return circuit_operation

    def _hack_to_add_desired_key_to_list_of_modified_keys(self, subcircuit: FrozenCircuit, majority_vote: MajorityVote) -> None:
        """must hack this because CircuitOperation does not recognize that nested MajorityVotes modify the 'desired_key'"""
        measurement_keys = set(subcircuit._measurement_key_objs_())
        measurement_keys.add(majority_vote.key)
        unfreeze = subcircuit.unfreeze

        def _unfreeze(copy: bool = True) -> Circuit:
            unfrozen = unfreeze(copy=copy)
            with_rescoped_keys = unfrozen._with_rescoped_keys_

            def _with_rescoped_keys(path: tuple[str, ...], bindable_keys: frozenset[MeasurementKey]):
                unmodified = with_rescoped_keys(path, bindable_keys)
                unmodified._measurement_key_objs_ = lambda: frozenset(measurement_keys)
                return unmodified

            unfrozen._with_rescoped_keys_ = _with_rescoped_keys
            return unfrozen

        subcircuit.unfreeze = _unfreeze

    @cached_property
    def _logical_operation_on_target(self) -> Circuit:
        try:
            return self._operation.target_encoding.encoding.get_operation_circuit(operation=self._operation.target_encoding.operation)
        except NotImplementedError as e:
            if self._operation.target_encoding:
                target_index = self._operation.target_encoding.operation.qubit_index
                code = LogicalEncodingIndex(
                    encoding=self._operation.target_encoding.encoding,
                    qubit_index_relative=target_index
                )
                if self._operation.target_encoding.operation.gate == LogicalGateLabel.H:
                    return self._universal_hadamard_type(code=code).get_hadamard_circuit()
                elif self._operation.target_encoding.operation.gate == LogicalGateLabel.T:
                    return self._universal_t_type(code=code).get_t_circuit()
            raise e

    @property
    def _measurer_type(self) -> type[Measurer]:
        return self._configuration.measurer_type

    @property
    def _universal_controlled_operation_type(self) -> type[UniversalControlledOperation]:
        return self._configuration.universal_controlled_operation_type

    @property
    def _universal_hadamard_type(self) -> type[UniversalHadamard]:
        return self._configuration.universal_hadamard_type

    @property
    def _universal_t_type(self) -> type[UniversalT]:
        return self._configuration.universal_t_type

    @property
    def _configuration(self) -> ConfigurationErrorCorrectingCode:
        return ConfigurationErrorCorrectingCodeManager().get_configuration()
