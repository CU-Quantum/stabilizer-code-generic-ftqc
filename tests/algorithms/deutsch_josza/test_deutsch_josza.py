import pytest
from cirq import LineQubit
from numpy.ma.core import allequal

from simulations.error_correcting_runner import ErrorCorrectingRunnerClifford
from simulations.error_correcting_simulator import ErrorCorrectingSimulatorStateVector
from stim_experiments.algorithms.deutsch_josza.deutsch_josza import DeutschJosza
from stim_experiments.custom_dataclasses.transformation_operation import TransformationGate, TransformationOperation
from stim_experiments.error_correcting_codes.support.multiple_cat_code.multiple_cat_code import MultipleCatCode
from tests.utilities import set_seed


@pytest.mark.slow
class TestDeutschJosza:
    @pytest.fixture(autouse=True, params=range(3))
    def _setup(self, request):
        set_seed(request.param)

    def test_deutsch_josza_constant(self):
        num_logical_qubits = 3
        encoding = MultipleCatCode(num_cats=3, num_qubits_per_cat=3)
        num_qubits_per_encoding = len(encoding.data_qubits)
        qubits = LineQubit.range(num_logical_qubits * num_qubits_per_encoding)
        logical_qubits = [encoding.create_new(qubits[i * num_qubits_per_encoding:(i + 1) * num_qubits_per_encoding])
                          for i in range(num_logical_qubits)]

        oracle = []
        algorithm = DeutschJosza(logical_qubits=logical_qubits, oracle=oracle, oracle_qubit_index=2)
        circuit = algorithm.get_circuit()

        runner = ErrorCorrectingRunnerClifford()
        result = runner.run_circuit(circuit, num_shots=5)
        for measurements in result.measurements_per_shot:
            assert allequal(measurements, [0, 0])

    def test_deutsch_josza_balanced(self):
        num_logical_qubits = 3
        encoding = MultipleCatCode(num_cats=3, num_qubits_per_cat=3)
        num_qubits_per_encoding = len(encoding.data_qubits)
        qubits = LineQubit.range(num_logical_qubits * num_qubits_per_encoding)
        logical_qubits = [encoding.create_new(qubits[i * num_qubits_per_encoding:(i + 1) * num_qubits_per_encoding])
                          for i in range(num_logical_qubits)]

        oracle = [
            TransformationOperation(gate=TransformationGate.CX, control_qubit_index=0, target_qubit_index=2),
            TransformationOperation(gate=TransformationGate.CX, control_qubit_index=1, target_qubit_index=2),
        ]
        algorithm = DeutschJosza(logical_qubits=logical_qubits, oracle=oracle, oracle_qubit_index=2)
        circuit = algorithm.get_circuit()

        runner = ErrorCorrectingRunnerClifford()
        result = runner.run_circuit(circuit, num_shots=5)
        for measurements in result.measurements_per_shot:
            assert not allequal(measurements, [0, 0])
