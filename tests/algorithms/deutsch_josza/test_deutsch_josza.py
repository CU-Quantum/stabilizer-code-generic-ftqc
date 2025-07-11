import pytest
from numpy.ma.core import allequal

from stim_experiments.algorithms.deutsch_josza.deutsch_josza import DeutschJosza
from stim_experiments.custom_dataclasses.transformation_operation import TransformationGate, TransformationOperation
from stim_experiments.error_correcting_codes.support.multiple_cat_code.multiple_cat_code import MultipleCatCode
from tests.utilities import set_configuration_to_reduce_ancilla_qubits, set_seed


@pytest.mark.slow
class TestDeutschJosza:
    @pytest.fixture(autouse=True)
    def _setup(self):
        set_seed(0)
        set_configuration_to_reduce_ancilla_qubits()

    def test_deutsch_josza_constant(self):
        num_qubits = 3
        logical_qubits = [MultipleCatCode(num_cats=3, num_qubits_per_cat=3) for _ in range(num_qubits)]
        oracle = []
        algorithm = DeutschJosza(logical_qubits=logical_qubits, oracle=oracle, oracle_qubit_index=2)
        result = algorithm.run_algorithm()
        assert allequal(list(result.logical_qubit_measurements.values()), [[0], [0]])

    def test_deutsch_josza_balanced(self):
        num_qubits = 3
        logical_qubits = [MultipleCatCode(num_cats=3, num_qubits_per_cat=3) for _ in range(num_qubits)]
        oracle = [
            TransformationOperation(gate=TransformationGate.CX, control_qubit_index=0, target_qubit_index=2),
            TransformationOperation(gate=TransformationGate.CX, control_qubit_index=1, target_qubit_index=2),
        ]
        algorithm = DeutschJosza(logical_qubits=logical_qubits, oracle=oracle, oracle_qubit_index=2)
        result = algorithm.run_algorithm()
        assert not allequal(list(result.logical_qubit_measurements.values()), [[0], [0]])
