import argparse
from datetime import datetime

import numpy as np
from cirq import CliffordSimulator, Result, depolarize

from custom_dataclasses.state_and_measurements import Measurements
from custom_dataclasses.transformation_operation import TransformationGate, TransformationOperation
from simulations.error_correcting_runner import ErrorCorrectingRunnerClifford
from stim_experiments.algorithms.deutsch_josza.deutsch_josza import DeutschJosza
from stim_experiments.error_correcting_codes.support.multiple_cat_code.multiple_cat_code import MultipleCatCode

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog='Deutsch-Josza Logical Error Rate Calculator',
        description='Runs the Deutsch-Josza algorithm using surface code and calculates the percentage of logical errors in the result.')
    parser.add_argument('-s', '--num-shots', type=int, default=1, help='Number of shots to run the algorithm for.')
    parser.add_argument('-q', '--num-input-qubits', type=int, default=2, help='Number of input qubits.')
    parser.add_argument('-d', '--surface-code-distance', type=int, default=5, help='Surface code distance.')
    parser.add_argument('-b', '--is-balanced', action="store_true", help='Surface code distance.')
    args = parser.parse_args()
    print(f"Running Deutsch-Josza Logical Error Rate Calculator with arguments: {args}")

    num_shots = args.num_shots
    num_input_qubits = args.num_input_qubits
    surface_code_distance = args.surface_code_distance
    is_balanced = args.is_balanced

    num_oracle_qubits = 1
    num_qubits = num_input_qubits + num_oracle_qubits
    oracle_qubit_index = num_input_qubits

    logical_qubits = [MultipleCatCode(num_cats=surface_code_distance, num_qubits_per_cat=surface_code_distance)
                      for _ in range(num_qubits)]
    oracle = [
        TransformationOperation(gate=TransformationGate.CX, control_qubit_index=i, target_qubit_index=oracle_qubit_index)
        for i in range(num_input_qubits)
    ] if is_balanced else []
    algorithm = DeutschJosza(logical_qubits=logical_qubits, oracle=oracle, oracle_qubit_index=oracle_qubit_index)
    circuit = algorithm.get_circuit()

    noise_model = depolarize(p=1e-4)
    simulator = ErrorCorrectingRunnerClifford()
    start_time = datetime.now()
    print(f"{start_time}: Start simulation")
    result: Measurements = simulator.run_circuit(circuit, num_shots=num_shots, noise_model=noise_model)
    print(f"    {datetime.now() - start_time}: End simulation")
    sum_measurements_per_shot = np.sum(result.measurements_per_shot, axis=1)
    nonzero_shots = np.count_nonzero(sum_measurements_per_shot)
    print(f"    Measurements per shot: {result.measurements_per_shot}")
    print(f"    {abs(num_shots * (not is_balanced) - nonzero_shots) / num_shots * 100:.1f}% success rate.")
