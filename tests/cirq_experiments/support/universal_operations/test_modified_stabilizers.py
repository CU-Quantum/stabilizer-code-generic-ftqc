from typing import Callable

import pytest
from cirq import Circuit, LineQubit, X, Y, Z

from cirq_experiments.custom_dataclasses.logical_operation import LogicalGateLabel, LogicalOperation
from cirq_experiments.custom_dataclasses.universal_operations_context import UniversalOperationsContext
from cirq_experiments.error_correcting_codes.generalized_shor_code_x_basis.generalized_shor_code_x_basis import GeneralizedShorCodeXBasis
from cirq_experiments.error_correcting_codes.generalized_shor_code.generalized_shor_code import GeneralizedShorCode
from cirq_experiments.support.universal_operations.universal_operations_utilities import \
    UniversalOperationsUtilities
from cirq_experiments.globals.active_encodings_store import ActiveEncodingsStore
from cirq_experiments.globals.fresh_ancillas_pool import FreshAncillasPool
from cirq_experiments.simulations.error_correcting_simulator import ErrorCorrectingSimulatorStateVector
from cirq_experiments.utilities.utilities import states_are_equal
from tests.cirq_experiments.utilities_for_tests import set_configuration_to_reduce_ancilla_qubits, set_seed


NOISY_CIRCUIT_TYPE = list[list[Circuit]]


class TestModifiedStabilizers:
    @pytest.fixture(autouse=True)
    def _setup(self):
        set_seed(0)
        set_configuration_to_reduce_ancilla_qubits()

        self._qubits = LineQubit.range(18)

    def test_no_errors(self):
        def build_noisy_circuit(encoding_circuit: Circuit, flip_circuit: NOISY_CIRCUIT_TYPE) -> Circuit:
            return Circuit(
                encoding_circuit,
                flip_circuit,
            )
        assert self._correct_with_modified_stabilizers(build_noisy_circuit=build_noisy_circuit)

    def test_x_error_on_first_qubit_of_third_cat_state_ghch_3_3(self):
        def build_noisy_circuit(encoding_circuit: Circuit, flip_circuit: NOISY_CIRCUIT_TYPE) -> Circuit:
            return Circuit(
                encoding_circuit,
                X(LineQubit(15)),
                flip_circuit,
            )
        assert self._correct_with_modified_stabilizers(build_noisy_circuit=build_noisy_circuit)

    def test_z_error_on_first_qubit_of_third_cat_state_ghch_3_3(self):
        def build_noisy_circuit(encoding_circuit: Circuit, flip_circuit: NOISY_CIRCUIT_TYPE) -> Circuit:
            return Circuit(
                encoding_circuit,
                Z(LineQubit(15)),
                flip_circuit,
            )
        assert self._correct_with_modified_stabilizers(build_noisy_circuit=build_noisy_circuit)

    def test_y_error_on_first_qubit_of_third_cat_state_ghch_3_3(self):
        def build_noisy_circuit(encoding_circuit: Circuit, flip_circuit: NOISY_CIRCUIT_TYPE) -> Circuit:
            return Circuit(
                encoding_circuit,
                Y(LineQubit(15)),
                flip_circuit,
            )
        assert self._correct_with_modified_stabilizers(build_noisy_circuit=build_noisy_circuit)

    def test_z_error_on_first_qubit_ghch_3_3(self):
        def build_noisy_circuit(encoding_circuit: Circuit, flip_circuit: NOISY_CIRCUIT_TYPE) -> Circuit:
            return Circuit(
                encoding_circuit,
                Z(LineQubit(0)),
                flip_circuit,
            )
        assert self._correct_with_modified_stabilizers(build_noisy_circuit=build_noisy_circuit)

    def test_z_error_on_first_cat_state_ghch_3_3(self):
        def build_noisy_circuit(encoding_circuit: Circuit, flip_circuit: NOISY_CIRCUIT_TYPE) -> Circuit:
            return Circuit(
                encoding_circuit,
                Z(LineQubit(0)),
                Z(LineQubit(9)),
                flip_circuit,
            )
        assert self._correct_with_modified_stabilizers(build_noisy_circuit=build_noisy_circuit)

    def test_error_in_each_block_ghch_3_3(self):
        def build_noisy_circuit(encoding_circuit: Circuit, flip_circuit: NOISY_CIRCUIT_TYPE) -> Circuit:
            return Circuit(
                encoding_circuit,
                Z(LineQubit(0)),
                X(LineQubit(9)),
                flip_circuit,
            )
        assert self._correct_with_modified_stabilizers(build_noisy_circuit=build_noisy_circuit)

    def test_z_error_on_second_subregister_ghch_3_3(self):
        def build_noisy_circuit(encoding_circuit: Circuit, flip_circuit: NOISY_CIRCUIT_TYPE) -> Circuit:
            return Circuit(
                encoding_circuit,
                Z(LineQubit(4)),
                flip_circuit,
            )
        assert self._correct_with_modified_stabilizers(build_noisy_circuit=build_noisy_circuit)

    def test_x_error_on_last_qubit_of_second_subregister_ghch_3_3(self):
        def build_noisy_circuit(encoding_circuit: Circuit, flip_circuit: NOISY_CIRCUIT_TYPE) -> Circuit:
            return Circuit(
                encoding_circuit,
                X(LineQubit(5)),
                flip_circuit,
            )
        assert self._correct_with_modified_stabilizers(build_noisy_circuit=build_noisy_circuit)

    def test_y_error_on_second_qubit_of_first_cat_state_ghch_3_3(self):
        def build_noisy_circuit(encoding_circuit: Circuit, flip_circuit: NOISY_CIRCUIT_TYPE) -> Circuit:
            return Circuit(
                encoding_circuit,
                Y(LineQubit(10)),
                flip_circuit,
            )
        assert self._correct_with_modified_stabilizers(build_noisy_circuit=build_noisy_circuit)

    def test_y_error_on_second_qubit_of_first_cat_state_ghch_3_3_after_second_subregister_and_before_correction(self):
        def build_noisy_circuit(encoding_circuit: Circuit, flip_circuit: NOISY_CIRCUIT_TYPE) -> Circuit:
            flip_circuit[1].insert(1, Y(LineQubit(10)))
            return Circuit(
                encoding_circuit,
                flip_circuit,
            )
        assert self._correct_with_modified_stabilizers(build_noisy_circuit=build_noisy_circuit, logical_operation=LogicalOperation(gate=LogicalGateLabel.Z, qubit_index=0))

    def test_reversed_registers(self):
        def build_noisy_circuit(encoding_circuit: Circuit, flip_circuit: NOISY_CIRCUIT_TYPE) -> Circuit:
            return Circuit(
                encoding_circuit,
                X(LineQubit(1)),
                flip_circuit,
            )

        control = GeneralizedShorCode(num_cats=3, num_qubits_per_cat=3, qubits=self._qubits[9:])
        target = GeneralizedShorCode(num_cats=3, num_qubits_per_cat=3, qubits=self._qubits[:9])
        self._correct_with_modified_stabilizers(build_noisy_circuit=build_noisy_circuit, control=control, target=target)

    def _correct_with_modified_stabilizers(
            self,
            build_noisy_circuit: Callable[[Circuit, NOISY_CIRCUIT_TYPE], Circuit],
            logical_operation: LogicalOperation = LogicalOperation(gate=LogicalGateLabel.X, qubit_index=0),
            control: GeneralizedShorCode = None,
            target: GeneralizedShorCode = None,
    ):
        FreshAncillasPool().set_first_ancilla_num(first_ancilla_num=len(self._qubits))
        simulator = ErrorCorrectingSimulatorStateVector()

        if control is None or target is None:
            control = GeneralizedShorCode(num_cats=3, num_qubits_per_cat=3, qubits=self._qubits[:9])
            target = GeneralizedShorCode(num_cats=3, num_qubits_per_cat=3, qubits=self._qubits[9:])
        x_operation_target = target.get_operation_circuit(operation=logical_operation)
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
                    generalized_shor_code_x_basis=GeneralizedShorCodeXBasis(num_cats=len(control.subregisters),
                                                                            num_qubits_per_cat=len(control.subregisters[0]),
                                                                            qubits=control.data_qubits, ),
                    generalized_shor_code=control,
                ),
                target_code=target,
            )
            no_errors_state = simulator.run_simulation(
                circuit=Circuit(
                    encoding_circuit,
                    flip_circuit,
                ),
                num_data_qubits=len(self._qubits),
            )

            circuit_with_error = build_noisy_circuit(encoding_circuit, flip_circuit)
            result = simulator.run_simulation(circuit_with_error, num_data_qubits=len(self._qubits))
            return states_are_equal(result.state, no_errors_state.state)
