from uuid import uuid4

from cirq import Circuit, CircuitOperation, KeyCondition, MeasurementKey, R, SWAP

from stim_experiments.custom_dataclasses.logical_operation import LogicalGateLabel, LogicalOperation
from stim_experiments.error_correcting_codes.support.controlled_single_qubit_gates_applier import \
    ControlledSingleQubitGatesApplier
from stim_experiments.error_correcting_codes.support.measurer.measurer import Measurer
from stim_experiments.error_correcting_codes.support.universal_hadamard.universal_hadamard_fault_tolerant.support.three_cat_subregister_parity_code_to_computational_logical import \
    ThreeCatSubregisterParityCodeToComputationalLogical
from stim_experiments.error_correcting_codes.support.universal_hadamard.universal_hadamard import UniversalHadamard
from stim_experiments.error_correcting_codes.three_cat_code.three_cat_code import ThreeCatCode
from stim_experiments.error_correcting_codes.three_cat_subregister_parity_code.three_cat_subregister_parity_code import \
    ThreeCatSubregisterParityCode
from stim_experiments.globals.error_correcting_code_configuration import ConfigurationErrorCorrectingCodeManager
from stim_experiments.globals.fresh_ancillas_pool import FreshAncillasPool


class UniversalHadamardFaultTolerant(UniversalHadamard):
    def get_hadamard_circuit(self) -> Circuit:
        measurement_key = MeasurementKey(f'UNIVERSAL_HADAMARD_MEASUREMENT_{uuid4().hex}')
        num_qubits_in_desired_encoding = len(self._code.data_qubits)
        with FreshAncillasPool().use_fresh_ancillas(num_ancillas=3 * num_qubits_in_desired_encoding) as ancilla_qubits:
            three_cat = ThreeCatCode(num_qubits_in_cat_state=num_qubits_in_desired_encoding, qubits=ancilla_qubits)
            uni_h = ThreeCatSubregisterParityCode(num_qubits_in_cat_state=num_qubits_in_desired_encoding, qubits=ancilla_qubits)
            new_encoding = self._code.create_new(qubits=uni_h.subregisters[0])
            to_computational_logical = ThreeCatSubregisterParityCodeToComputationalLogical(
                three_cat_subregister_parity_code=uni_h, desired_encoding=self._code)
            logical_x, logical_z = (list(self._code.get_operation_circuit(operation=LogicalOperation(gate=gate, qubit_index=0)).all_operations())  # allow multi qubit encodings
                                    for gate in (LogicalGateLabel.X, LogicalGateLabel.Z))
            return Circuit(
                three_cat.encode_logical_qubit(),
                [
                    ControlledSingleQubitGatesApplier(operations=logical_x, controls=subregister[:len(logical_x)]).get_circuit()
                    for subregister in three_cat.subregisters
                ],
                to_computational_logical.get_circuit(),
                self._measurer_type(operations=logical_z, measurement_key=measurement_key).get_measurement_circuit(),
                CircuitOperation(
                    new_encoding.get_operation_circuit(LogicalOperation(gate=LogicalGateLabel.Z, qubit_index=0)).freeze()
                ).with_classical_controls(KeyCondition(key=measurement_key)),
                [
                    SWAP(new_encoding.data_qubits[i], self._code.data_qubits[i])
                    for i in range(len(new_encoding.data_qubits))
                ],
                [R(ancilla) for ancilla in ancilla_qubits]
            )


    @property
    def _measurer_type(self) -> type[Measurer]:
        return ConfigurationErrorCorrectingCodeManager().get_configuration().measurer_type
