from stim_experiments.globals.fresh_ancillas_pool import FreshAncillasPool

# Stim Experiments

A Python package for quantum error correction experiments using Cirq and Stim.

## Description

This project provides tools and utilities for experimenting with quantum error correction codes, with a focus on stabilizer circuits. It uses Cirq for quantum circuit creation and simulation, and Stim for fast stabilizer circuit simulation.

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/stim_experiments.git
cd stim_experiments
```

2. Install the required dependencies:
```bash
pip install -r requirements.txt
```

## Getting Started with Cirq Simulator

### Basic Circuit Creation and Simulation

Here's a simple example of creating and simulating a quantum circuit using Cirq:

```python
from cirq import Circuit, H, X, LineQubit, final_state_vector

# Create qubits
qubits = LineQubit.range(2)

# Create a circuit
circuit = Circuit(
    H(qubits[0]),                    # Apply Hadamard gate to the first qubit
    X(qubits[1]).controlled_by(qubits[0])  # Apply CNOT gate (controlled-X)
)

# Simulate the circuit
result = circuit.final_state_vector()

# Print the result
print("Final state vector:")
print(result)
```

This example creates a Bell state, which is a maximally entangled state between two qubits.

### Using the Project's Simulator for Error Correction Simulation

The project provides a `LogicalOperationsCircuitCreator` for creating circuits with logical operations:

```python
from cirq import LineQubit
from stim_experiments.custom_dataclasses.transformation_operation import TransformationGate, TransformationOperation
from stim_experiments.error_correcting_codes.stabilizer_standardized_code.stabilizer_standardized_code import StabilizerStandardizedCode
from stim_experiments.simulators.simulator_using_circuits.logical_operations_circuit_creator import LogicalOperationsCircuitCreator
from stim_experiments.error_correcting_codes.error_correcting_code_utilities import get_error_correcting_code_utilities
from stim_experiments.utilities.utilities import KET_ZERO_STATE_VECTOR
from stim_experiments.utilities.predefined_check_matrix_values import get_check_matrix_values_5_qubit

# Create qubits for two logical qubits
# The 5-qubit code requires 5 physical qubits per logical qubit
qubits = LineQubit.range(10)  # 5 qubits for each logical qubit

# Create encodings using the five qubit code
standardized_five_qubit = StabilizerStandardizedCode(generators=get_check_matrix_values_5_qubit())
encodings = [
    standardized_five_qubit.create_new(qubits=qubits[:5]),
    standardized_five_qubit.create_new(qubits=qubits[5:])
]

# Define operations (creating a Bell state with measurement)
operations = [
    TransformationOperation(gate=TransformationGate.H, target_qubit_index=0),
    TransformationOperation(gate=TransformationGate.CX, target_qubit_index=1, control_qubit_index=0),
    TransformationOperation(gate=TransformationGate.M, target_qubit_index=1),  # Measure the second qubit
]

# Create the simulator
simulator = LogicalOperationsCircuitCreator(encodings=encodings, operations=operations)

# Get the simulation circuit
circuit = simulator.get_simulation_circuit()

# Simulate the circuit
utilities = get_error_correcting_code_utilities(state=KET_ZERO_STATE_VECTOR)
result = utilities.get_state_after_circuit(
    circuit=circuit,
    num_data_qubits=len(simulator.data_qubits),
)

# Analyze the result
print("Final state:", result.state)
print("Measurements:", result.measurements)
```

## Configuration Settings

The project provides a configuration system that allows you to customize various aspects of the error correction process. You can access and modify the configuration using the `ConfigurationErrorCorrectingCodeManager`:

```python
from stim_experiments.globals.error_correcting_code_configuration import ConfigurationErrorCorrectingCodeManager
from stim_experiments.custom_enums.universal_hadamard_type import UniversalHadamardType
from stim_experiments.custom_enums.universal_controlled_operation_type import UniversalControlledOperationType
from stim_experiments.error_correcting_codes.support.measurer.measurer_with_single_qubit import MeasurerWithSingleQubit
from stim_experiments.error_correcting_codes.support.cat_state_creator.cat_state_creator_cx_from_first_qubit import CatStateCreatorCxFromFirstQubit

# Get the configuration
configuration = ConfigurationErrorCorrectingCodeManager().get_configuration()

# Modify configuration settings
configuration.universal_hadamard_type = UniversalHadamardType.SINGLE_ANCILLA
configuration.universal_controlled_operation_type = UniversalControlledOperationType.SINGLE_ANCILLA
configuration.measurer_type = MeasurerWithSingleQubit
configuration.cat_state_creator_type = CatStateCreatorCxFromFirstQubit
configuration.seed = 42  # Set a random seed for reproducibility
```

Available configuration options:

1. `measurer_type`: Type of measurer to use (default: `FaultTolerantMeasurer`)
2. `cat_state_creator_type`: Type of cat state creator to use (default: `CatStateCreatorFlagPattern`)
3. `universal_hadamard_type`: Type of universal Hadamard implementation (default: `UniversalHadamardType.FAULT_TOLERANT`)
4. `universal_controlled_operation_type`: Type of universal controlled operation implementation (default: `UniversalControlledOperationType.FAULT_TOLERANT`)
5. `universal_t_type`: Type of universal T implementation (default: `UniversalTType.FAULT_TOLERANT`)
6. `seed`: Optional seed for random number generation (default: `None`)


## Creating Your Own Error Correcting Code

You can create your own error correcting code by extending the `ErrorCorrectingCode` abstract base class and implementing the required methods:

```python
from cirq import Circuit, LineQubit, R, X, Z
from typing import Optional

from stim_experiments.custom_dataclasses.logical_operation import LogicalGateLabel, LogicalOperation
from stim_experiments.custom_dataclasses.state_encoding import StateEncoding
from stim_experiments.globals.fresh_ancillas_pool import FreshAncillasPool
from stim_experiments.error_correcting_codes.error_correcting_code.error_correcting_code import ErrorCorrectingCode

class MyCustomCode(ErrorCorrectingCode):
    def __init__(self, num_logical_qubits: int = 1, qubits: Optional[list[LineQubit]] = None):
        # For this example, we'll use a simple 3-qubit repetition code
        super().__init__(num_data_qubits=3 * num_logical_qubits,
                         num_logical_qubits=num_logical_qubits,
                         qubits=qubits)

    def encode_logical_qubit(self) -> StateEncoding:
        # Implement the encoding circuit for your code
        # For a 3-qubit repetition code, we could use CNOT gates to copy the state
        circuit = Circuit()
        for i in range(self._num_logical_qubits):
            base_idx = i * 3
            circuit.append([
                X(self.data_qubits[base_idx + 1]).controlled_by(self.data_qubits[base_idx]),
                X(self.data_qubits[base_idx + 2]).controlled_by(self.data_qubits[base_idx])
            ])
        return StateEncoding(circuit=circuit)

    def get_error_correction_circuit(self) -> Circuit:
        # Implement error correction for your code
        # For a 3-qubit repetition code, we would use majority voting
        circuit = Circuit()
        # FreshAncillasPool allows you to pull fresh or unused ancilla qubits. 
        with FreshAncillasPool().use_fresh_ancillas(num_ancillas=2) as ancilla_quibts:
            # Add error correction operations
            Circuit.append(...)
            # You must ensure the ancilla qubits return to the |0> state before exiting the FreshAncillasPool context.
            Circuit.append(R(ancilla for ancilla in ancilla_quibts))
            return circuit

    def _perform_get_operation_circuit(self, operation: LogicalOperation) -> Optional[Circuit]:
        # Implement logical operations for your code
        if operation.gate == LogicalGateLabel.X:
            # Apply X to all physical qubits representing the logical qubit
            base_idx = operation.qubit_index * 3
            return Circuit([
                X(self.data_qubits[base_idx]),
                X(self.data_qubits[base_idx + 1]),
                X(self.data_qubits[base_idx + 2])
            ])
        elif operation.gate == LogicalGateLabel.Z:
            # For a bit-flip code, Z is applied to any one qubit
            base_idx = operation.qubit_index * 3
            return Circuit(Z(self.data_qubits[base_idx]))
        elif operation.gate == LogicalGateLabel.H:
            # If the code has an efficient Hadamard operation, you can include it in here. 
            # Otherwise, the simulator will use the universal hadamard type set in the configuration.
            return None
        elif operation.gate == LogicalGateLabel.T:
            # If the code has an efficient T operation, you can include it in here. 
            # Otherwise, the simulator will use the universal T type set in the configuration.
            return None
        return None  # Other operations not implemented.
```

You can then use your custom code with the simulator:

```python
from stim_experiments.custom_dataclasses.transformation_operation import TransformationGate, TransformationOperation
from stim_experiments.simulators.simulator_using_circuits.logical_operations_circuit_creator import LogicalOperationsCircuitCreator
from stim_experiments.error_correcting_codes.error_correcting_code_utilities import get_error_correcting_code_utilities
from stim_experiments.utilities.utilities import KET_ZERO_STATE_VECTOR

# Create qubits for two logical qubits (3 physical qubits per logical qubit)
qubits = LineQubit.range(6)

# Create encodings using your custom code
encodings = [
    MyCustomCode(num_logical_qubits=1, qubits=qubits[:3]),
    MyCustomCode(num_logical_qubits=1, qubits=qubits[3:])
]

# Define operations
operations = [
    TransformationOperation(gate=TransformationGate.H, target_qubit_index=0),
    TransformationOperation(gate=TransformationGate.CX, target_qubit_index=1, control_qubit_index=0),
    TransformationOperation(gate=TransformationGate.M, target_qubit_index=1),
]

# Create the simulator and run the simulation
simulator = LogicalOperationsCircuitCreator(encodings=encodings, operations=operations)
circuit = simulator.get_simulation_circuit()
utilities = get_error_correcting_code_utilities(state=KET_ZERO_STATE_VECTOR)
result = utilities.get_state_after_circuit(
    circuit=circuit,
    num_data_qubits=len(simulator.data_qubits),
)
```

## License

This project is licensed under the [MIT License](LICENSE).
