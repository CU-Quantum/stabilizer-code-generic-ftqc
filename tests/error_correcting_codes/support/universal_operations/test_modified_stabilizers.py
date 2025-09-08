import pytest
from cirq import Circuit, LineQubit, X, Y, Z

from stim_experiments.custom_dataclasses.logical_operation import LogicalGateLabel, LogicalOperation
from stim_experiments.custom_dataclasses.universal_operations_context import UniversalOperationsContext
from stim_experiments.error_correcting_codes.cat_parity_code.cat_parity_code import CatParityCode
from stim_experiments.error_correcting_codes.multiple_cat_code.multiple_cat_code import MultipleCatCode
from stim_experiments.error_correcting_codes.support.universal_operations.universal_operations_utilities import \
    UniversalOperationsUtilities
from stim_experiments.globals.active_encodings_store import ActiveEncodingsStore
from stim_experiments.globals.fresh_ancillas_pool import FreshAncillasPool
from stim_experiments.simulations.error_correcting_simulator import ErrorCorrectingSimulatorStateVector
from stim_experiments.utilities.utilities import states_are_equal
from tests.utilities_for_tests import set_configuration_to_reduce_ancilla_qubits, set_seed


class TestModifiedStabilizers:
    @pytest.fixture(autouse=True)
    def _setup(self):
        set_seed(0)
        set_configuration_to_reduce_ancilla_qubits()

    def test_no_errors(self):
        error_circuit = Circuit()
        assert self._correct_with_modified_stabilizers(error_circuit=error_circuit)

    def test_x_error_on_first_qubit_of_third_cat_state_ghch_3_3(self):
        error_circuit = Circuit(
            X(LineQubit(15))
        )
        assert self._correct_with_modified_stabilizers(error_circuit=error_circuit)

    def test_z_error_on_first_qubit_of_third_cat_state_ghch_3_3(self):
        error_circuit = Circuit(
            Z(LineQubit(15))
        )
        assert self._correct_with_modified_stabilizers(error_circuit=error_circuit)

    def test_y_error_on_first_qubit_of_third_cat_state_ghch_3_3(self):
        error_circuit = Circuit(
            Y(LineQubit(15))
        )
        assert self._correct_with_modified_stabilizers(error_circuit=error_circuit)

    def test_z_error_on_first_qubit_ghch_3_3(self):
        error_circuit = Circuit(
            Z(LineQubit(0))
        )
        assert self._correct_with_modified_stabilizers(error_circuit=error_circuit)

    def test_z_error_on_first_cat_state_ghch_3_3(self):
        error_circuit = Circuit(
            Z(LineQubit(9))
        )
        assert self._correct_with_modified_stabilizers(error_circuit=error_circuit)

    def test_overcorrection_ghch_3_3(self):
        more_than_half_distance_phase_errors = Circuit(
            Z(LineQubit(0)),
            Z(LineQubit(3)),
        )
        assert self._correct_with_modified_stabilizers(error_circuit=more_than_half_distance_phase_errors)

    def _correct_with_modified_stabilizers(self, error_circuit: Circuit):
        qubits = LineQubit.range(18)
        FreshAncillasPool().set_first_ancilla_num(first_ancilla_num=len(qubits))
        simulator = ErrorCorrectingSimulatorStateVector()

        control = MultipleCatCode(num_cats=3, num_qubits_per_cat=3, qubits=qubits[:9])
        target = MultipleCatCode(num_cats=3, num_qubits_per_cat=3, qubits=qubits[9:])
        x_operation_target = target.get_operation_circuit(operation=LogicalOperation(gate=LogicalGateLabel.X, qubit_index=0))
        target_operations = list(x_operation_target.all_operations())

        with ActiveEncodingsStore(additional_tracked_encodings=[target]):
            encoding_circuit = Circuit(
                control.encode_logical_qubit(),
                target.encode_logical_qubit(),
            )
            flip_circuit = UniversalOperationsUtilities.c_operations_helpers_to_data(
                operations=target_operations,
                context=UniversalOperationsContext(
                    ancilla_qubits=[],
                    cat_parity_code=CatParityCode(num_cats=len(control.subregisters),
                                                  num_qubits_per_cat=len(control.subregisters[0]),
                                                  qubits=control.data_qubits,),
                    multiple_cat_code=control,
                ),
                target_code=target,
            )
            no_errors_state = simulator.run_simulation(
                circuit=Circuit(
                    encoding_circuit,
                    flip_circuit,
                ),
                num_data_qubits=len(qubits))

            circuit_with_error = Circuit(
                encoding_circuit,
                error_circuit,
                flip_circuit,
            )
            result = simulator.run_simulation(circuit_with_error, num_data_qubits=len(qubits))
            return states_are_equal(result.state, no_errors_state.state)
