from typing import Optional

from cirq import Circuit, I, LineQubit

from stim_experiments.custom_dataclasses.correction_circuit import CorrectionCircuit
from stim_experiments.custom_dataclasses.logical_operation import LogicalOperation
from stim_experiments.error_correcting_codes.error_correcting_code.error_correcting_code import ErrorCorrectingCode
from stim_experiments.globals.active_encodings_store import ActiveEncodingsStore


class CodeStub(ErrorCorrectingCode):
    def __init__(self, qubits: Optional[list[LineQubit]] = None,):
        super().__init__(num_data_qubits=1,
                         num_logical_qubits=1,
                         qubits=qubits)

    def encode_logical_qubit(self) -> Circuit:
        pass

    def get_error_correction_circuit(self) -> CorrectionCircuit:
        return CorrectionCircuit(
            syndrome_circuit=Circuit(I(self.data_qubits[0]))
        )

    def _perform_get_operation_circuit(self, operation: LogicalOperation) -> Optional[Circuit]:
        pass


class TestActiveEncodingsStore:
    def test_no_tracked_encodings(self):
        with ActiveEncodingsStore(additional_tracked_encodings=[]) as encodings_store:
            circuit = encodings_store.get_all_correction_circuits()
            assert circuit == Circuit()

    def test_register_encoding(self):
        qubits = LineQubit.range(1)
        code = CodeStub(qubits=qubits)
        with ActiveEncodingsStore(additional_tracked_encodings=[code]) as encodings_store:
            circuit = encodings_store.get_all_correction_circuits()
            assert circuit == Circuit(I(qubits[0]))

    def test_register_multiple_encodings(self):
        qubits = LineQubit.range(2)
        code = CodeStub(qubits=qubits[:1])
        code2 = CodeStub(qubits=qubits[1:])
        with ActiveEncodingsStore(additional_tracked_encodings=[code, code2]) as encodings_store:
            circuit = encodings_store.get_all_correction_circuits()
            assert list(circuit.all_operations()) == list(Circuit([I(qubit) for qubit in qubits]).all_operations())

    def test_register_using_multiple_stores(self):
        qubits = LineQubit.range(2)
        codes = [CodeStub(qubits=[qubit]) for qubit in qubits]
        with ActiveEncodingsStore(additional_tracked_encodings=codes[:1]) as encodings_store:
            circuit = encodings_store.get_all_correction_circuits()
            assert list(circuit.all_operations()) == list(Circuit([I(qubit) for qubit in qubits[:1]]).all_operations())

            with ActiveEncodingsStore(additional_tracked_encodings=codes[1:]) as encodings_store2:
                circuit = encodings_store2.get_all_correction_circuits()
                assert list(circuit.all_operations()) == list(Circuit([I(qubit) for qubit in qubits]).all_operations())

            circuit = encodings_store.get_all_correction_circuits()
            assert list(circuit.all_operations()) == list(Circuit([I(qubit) for qubit in qubits[:1]]).all_operations())
