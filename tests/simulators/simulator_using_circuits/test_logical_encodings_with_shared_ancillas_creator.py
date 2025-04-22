from typing import List, Optional

from cirq import Circuit, LineQubit

from stim_experiments.custom_dataclasses.logical_operation import LogicalGateLabel, LogicalOperation
from stim_experiments.error_correcting_codes.error_correcting_code.error_correcting_code import ErrorCorrectingCode
from stim_experiments.simulators.simulator_using_circuits.logical_encodings_with_shared_ancillas_creator import \
    LogicalEncodingsWithSharedAncillasCreatorMultipleCodes, LogicalEncodingsWithSharedAncillasCreatorSingleCode
from stim_experiments.utilities import KET_ZERO_STATE_VECTOR, TYPE_STATE_VECTOR_OR_DENSITY_MATRIX, tensor


class CodeStub(ErrorCorrectingCode):
    def __init__(self,
                 num_logical_qubits: int = 1, 
                 num_ancilla_qubits: int = 0, 
                 qubit_start_index: int = 0,
                 provided_ancilla_qubits: Optional[List[LineQubit]] = None):
        super().__init__(num_data_qubits=num_logical_qubits,
                         num_ancilla_qubits=num_ancilla_qubits,
                         num_logical_qubits=num_logical_qubits,
                         initial_logical_qubit_state=KET_ZERO_STATE_VECTOR,
                         qubit_start_index=qubit_start_index,
                         provided_ancilla_qubits=provided_ancilla_qubits
                         )

    def encode_logical_qubit(self) -> TYPE_STATE_VECTOR_OR_DENSITY_MATRIX:
        pass

    def get_error_correction_circuit(self) -> Circuit:
        pass

    def _perform_get_operation_circuit(self, operation: LogicalOperation) -> Optional[Circuit]:
        pass

    @property
    def _implemented_operations(self) -> List[LogicalGateLabel]:
        pass


class TestLogicalEncodingsWithSharedAncillasCreatorSingleCode:
    def test_creates_enough_encodings(self):
        code = CodeStub(num_logical_qubits=2)
        creator = LogicalEncodingsWithSharedAncillasCreatorSingleCode(error_correcting_code=code, num_logical_qubits_needed=5)
        encodings = creator.create_encodings()
        assert len(encodings.encodings) == 3
    
    def test_shared_ancilla_qubits(self):
        code = CodeStub(num_logical_qubits=1, num_ancilla_qubits=2)
        creator = LogicalEncodingsWithSharedAncillasCreatorSingleCode(error_correcting_code=code,
                                                                      num_logical_qubits_needed=2)
        encodings = creator.create_encodings()
        assert len(encodings.encodings) == 2
        assert all(encoding.ancilla_qubits == encodings.ancillas for encoding in encodings.encodings)


class TestLogicalEncodingsWithSharedAncillasCreatorMultipleCodes:
    def test_creates_same_number_of_encodings(self):
        codes = [CodeStub(), CodeStub()]
        creator = LogicalEncodingsWithSharedAncillasCreatorMultipleCodes(error_correcting_codes=codes)
        encodings = creator.create_encodings()
        assert len(encodings.encodings) == 2

    def test_shared_ancilla_qubits(self):
        codes_with_different_num_ancillas = [
            CodeStub(num_logical_qubits=1, num_ancilla_qubits=1),
            CodeStub(num_logical_qubits=1, num_ancilla_qubits=2)
        ]
        creator = LogicalEncodingsWithSharedAncillasCreatorMultipleCodes(error_correcting_codes=codes_with_different_num_ancillas)
        encodings = creator.create_encodings()
        assert len(encodings.encodings) == 2
        assert all(ancilla in encodings.ancillas for encoding in encodings.encodings for ancilla in encoding.ancilla_qubits)
