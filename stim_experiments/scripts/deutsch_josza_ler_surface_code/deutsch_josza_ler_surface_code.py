import argparse
from datetime import datetime

from stim_experiments.algorithms.deutsch_josza.deutsch_josza import DeutschJosza
from stim_experiments.error_correcting_codes.error_correcting_code_utilities import ErrorCorrectingCodeUtilitiesMultiGpu
from stim_experiments.error_correcting_codes.support.multiple_cat_code.multiple_cat_code import MultipleCatCode

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog='Deutsch-Josza Logical Error Rate Calculator',
        description='Runs the Deutsch-Josza algorithm using surface code and calculates the percentage of logical errors in the result.')
    parser.add_argument('-s', '--num-shots', type=int, default=1000, help='Number of shots to run the algorithm for.')
    parser.add_argument('-q', '--num-input-qubits', type=int, default=2, help='Number of input qubits.')
    parser.add_argument('-d', '--surface-code-distance', type=int, default=5, help='Surface code distance.')
    args = parser.parse_args()

    num_shots = args.num_shots
    num_input_qubits = args.num_input_qubits
    surface_code_distance = args.surface_code_distance
    num_oracle_qubits = 1
    num_qubits = num_input_qubits + num_oracle_qubits
    oracle_qubit_index = num_input_qubits

    logical_qubits = [MultipleCatCode(num_cats=surface_code_distance, num_qubits_per_cat=surface_code_distance)
                      for _ in range(num_qubits)]
    # oracle_balanced = [
    #     TransformationOperation(gate=TransformationGate.CX, control_qubit_index=i, target_qubit_index=oracle_qubit_index)
    #     for i in range(num_input_qubits)
    # ]
    oracle_constant = []
    algorithm = DeutschJosza(logical_qubits=logical_qubits, oracle=oracle_constant, oracle_qubit_index=oracle_qubit_index)
    circuit = algorithm.get_circuit()

    successful_shots = 0
    for shot in range(num_shots):
        start_time = datetime.now()
        print(f"{start_time}: Shot {shot + 1}/{num_shots}")

        utilities = ErrorCorrectingCodeUtilitiesMultiGpu()
        result = utilities.get_state_after_circuit(
            circuit=circuit,
            num_data_qubits=num_qubits,
        )

        end_time = datetime.now()
        print(f"    {end_time} ({end_time - start_time}): {result.logical_qubit_measurements}")
        if any(measurement for measurements in result.logical_qubit_measurements.values() for measurement in measurements):
            print("    Logical error detected.")
        else:
            print("    No logical error detected.")
        print(f"    {successful_shots / num_shots * 100:.1f}% successful shots so far.")
