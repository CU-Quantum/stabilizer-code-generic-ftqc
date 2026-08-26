# Stabilizer Code-Generic Universal Fault-Tolerant Quantum Computation

A Python framework for fault-tolerant quantum computing (FTQC) and quantum error correction (QEC) experiments across arbitrary stabilizer codes using [Cirq](https://quantumai.google/cirq) and [Stim](https://github.com/quantumlib/Stim).

---

## Overview

This repository provides tools, circuits, and simulation pipelines for:
- **Generic Stabilizer Codes**: Arbitrary stabilizer codes specified by check matrices in standard or non-standard forms (e.g. 5-qubit code, Steane code, Shor code, Dodecacode, Golay [[23,1,7]] code, Tetrahedral code).
- **Universal Fault-Tolerant Operations**: Ancilla-assisted fault-tolerant logical Clifford + T gates and universal controlled-flip operations.
- **Stim Experiments & Monte Carlo Simulations**: High-performance error threshold and logical error rate simulations using Stim, PyMatching, and LDPC decoders.
- **Cirq State Vector Simulations**: Exact quantum state verification and FTQC algorithm simulations (e.g. Deutsch-Jozsa, logical state preparation, and syndrome extraction).

---

## Repository Structure

```
├── docs/                     # Documentation and theoretical notes
├── results/                  # Simulation data and results
├── src/
│   ├── cirq_experiments/     # Cirq-based quantum error correction and FTQC framework
│   │   ├── algorithms/       # FTQC algorithm circuits (e.g. Deutsch-Jozsa)
│   │   ├── error_correcting_codes/ # Code implementations (Five-qubit, Steane, Golay, Shor, etc.)
│   │   ├── simulations/      # State-vector and error-correcting simulation runners
│   │   ├── support/          # Ancilla pools, cat state creators, measurers, universal gates
│   │   └── utilities/        # Mathematical utilities and state verification
│   ├── stim_experiments/     # Stim-based threshold and circuit-level noise simulations
│   │   ├── circuits/         # Noise-aware Stim circuit builders
│   │   └── scripts/          # Parameter sweeps, decoder benchmarking, and plotting scripts
│   └── predefined_check_matrix_values.py # Predefined stabilizer check matrices
└── tests/                    # Comprehensive test suite
```

---

## Installation

### Prerequisites
- Python 3.10+
- A virtual environment is recommended

### Setup
```bash
# Clone the repository
git clone https://github.com/CU-Quantum/stabilizer-code-generic-ftqc.git
cd stabilizer-code-generic-ftqc

# Create and activate virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install dependencies and package in editable mode
pip install -e .
```

---

## Quick Start

### 1. Basic Circuit Simulation (Cirq)

```python
import cirq

# Create qubits and circuit
qubits = cirq.LineQubit.range(2)
circuit = cirq.Circuit(
    cirq.H(qubits[0]),
    cirq.CNOT(qubits[0], qubits[1]),
)

# Simulate
simulator = cirq.Simulator()
result = simulator.simulate(circuit)
print("State vector:", result.final_state_vector)
```

### 2. Logical State Preparation & Operations

Create and simulate logical qubits encoded with arbitrary stabilizer codes:

```python
import cirq
from cirq_experiments.algorithms.logical_operations_circuit_creator import (
    LogicalOperationsCircuitCreator,
)
from cirq_experiments.custom_dataclasses.transformation_operation import (
    TransformationGate,
    TransformationOperation,
)
from cirq_experiments.error_correcting_codes.stabilizer_standardized_code.stabilizer_standardized_code import (
    StabilizerStandardizedCode,
)
from cirq_experiments.simulations.error_correcting_simulator_state_vector import (
    ErrorCorrectingSimulatorStateVector,
)
from predefined_check_matrix_values import get_check_matrix_values_5_qubit

# Initialize physical qubits (5 qubits per logical qubit for the 5-qubit code)
qubits = cirq.LineQubit.range(10)

# Create 5-qubit stabilizer code encodings
code = StabilizerStandardizedCode(generators=get_check_matrix_values_5_qubit())
encodings = [
    code.create_new(qubits=qubits[:5]),
    code.create_new(qubits=qubits[5:]),
]

# Define logical operations (e.g. Logical Bell State)
operations = [
    TransformationOperation(gate=TransformationGate.H, target_qubit_index=0),
    TransformationOperation(gate=TransformationGate.CX, target_qubit_index=1, control_qubit_index=0),
    TransformationOperation(gate=TransformationGate.M, target_qubit_index=1),
]

# Build and simulate the logical circuit
creator = LogicalOperationsCircuitCreator(encodings=encodings, operations=operations)
circuit = creator.get_simulation_circuit()

simulator = ErrorCorrectingSimulatorStateVector()
result = simulator.run_simulation(
    circuit=circuit,
    num_data_qubits=len(creator.data_qubits),
)

print("Final state:", result.state)
print("Logical measurements:", result.logical_qubit_measurements)
```

---

## Configuration

Customize measurer implementations, cat state creation strategies, and universal operations via `ConfigurationErrorCorrectingCodeManager`:

```python
from cirq_experiments.globals.error_correcting_code_configuration import (
    ConfigurationErrorCorrectingCodeManager,
)
from cirq_experiments.support.cat_state_creator.cat_state_creator_cx_from_first_qubit.cat_state_creator_cx_from_first_qubit import (
    CatStateCreatorCxFromFirstQubit,
)
from cirq_experiments.support.measurer.measurer_with_single_qubit_sequential import (
    MeasurerWithSingleQubitSequential,
)
from cirq_experiments.support.universal_operations.universal_controlled_flip.universal_controlled_flip_single_ancilla import (
    UniversalControlledOperationSingleAncilla,
)
from cirq_experiments.support.universal_operations.universal_hadamard.universal_hadamard_single_ancilla import (
    UniversalHadamardSingleAncilla,
)
from cirq_experiments.support.universal_operations.universal_t.universal_t_single_ancilla import (
    UniversalTSingleAncilla,
)

config = ConfigurationErrorCorrectingCodeManager().get_configuration()

# Configure execution strategies
config.measurer_type = MeasurerWithSingleQubitSequential
config.cat_state_creator_type = CatStateCreatorCxFromFirstQubit
config.universal_hadamard_type = UniversalHadamardSingleAncilla
config.universal_controlled_operation_type = UniversalControlledOperationSingleAncilla
config.universal_t_type = UniversalTSingleAncilla
config.seed = 42
```

### Available Configuration Options

| Option | Type | Default | Description |
|---|---|---|---|
| `measurer_type` | `type[Measurer]` | `FaultTolerantMeasurer` | Strategy for stabilizer / parity measurement |
| `cat_state_creator_type` | `type[CatStateCreator]` | `CatStateCreatorFlagPattern` | Cat state preparation protocol |
| `universal_hadamard_type` | `type[UniversalHadamard]` | `UniversalHadamardFaultTolerant` | Logical Hadamard implementation |
| `universal_controlled_operation_type` | `type[UniversalControlledOperation]` | `UniversalControlledOperationFaultTolerant` | Universal controlled gate strategy |
| `universal_t_type` | `type[UniversalT]` | `UniversalTFaultTolerant` | Fault-tolerant logical T gate strategy |
| `num_cat_states` | `int` | `3` | Number of cat states for Generalized Shor Code |
| `seed` | `Optional[int]` | `None` | Random seed for simulation reproducibility |
| `majority_vote_repetitions` | `int` | `3` | Syndrome measurement repetitions for majority voting |

---

## Custom Stabilizer Codes

Extend `ErrorCorrectingCode` or instantiate `StabilizerStandardizedCode` with custom check matrices:

```python
from typing import Optional
import cirq
from cirq_experiments.custom_dataclasses.correction_circuit import CorrectionCircuit
from cirq_experiments.custom_dataclasses.logical_operation import LogicalGateLabel, LogicalOperation
from cirq_experiments.error_correcting_codes.error_correcting_code import ErrorCorrectingCode
from cirq_experiments.globals.fresh_ancillas_pool import FreshAncillasPool


class My3QubitRepetitionCode(ErrorCorrectingCode):
    def __init__(self, num_logical_qubits: int = 1, qubits: Optional[list[cirq.LineQubit]] = None):
        super().__init__(
            num_data_qubits=3 * num_logical_qubits,
            num_logical_qubits=num_logical_qubits,
            qubits=qubits,
        )

    def encode_logical_qubit(self) -> cirq.Circuit:
        circuit = cirq.Circuit()
        for i in range(self._num_logical_qubits):
            base = i * 3
            circuit.append([
                cirq.CNOT(self.data_qubits[base], self.data_qubits[base + 1]),
                cirq.CNOT(self.data_qubits[base], self.data_qubits[base + 2]),
            ])
        return circuit

    def get_error_correction_circuit(self) -> CorrectionCircuit:
        circuit = CorrectionCircuit()
        with FreshAncillasPool().use_fresh_ancillas(num_ancillas=2) as ancillas:
            circuit.syndrome_circuit.append([cirq.reset(a) for a in ancillas])
            # Add stabilizer measurement and correction logic
        return circuit

    def _perform_get_operation_circuit(self, operation: LogicalOperation) -> Optional[cirq.Circuit]:
        if operation.gate == LogicalGateLabel.X:
            base = operation.qubit_index * 3
            return cirq.Circuit(cirq.X(q) for q in self.data_qubits[base:base + 3])
        elif operation.gate == LogicalGateLabel.Z:
            base = operation.qubit_index * 3
            return cirq.Circuit(cirq.Z(self.data_qubits[base]))
        return None
```

---

## Experiments & Benchmarking

### Stim Simulations
- **5-Qubit Code**: `src/stim_experiments/scripts/five_qubit_code/`
- **Dodecacode**: `src/stim_experiments/scripts/dodecacode/`
- **Plotting & Analysis**: `src/stim_experiments/scripts/`

Run a sample Stim simulation script:
```bash
python src/stim_experiments/scripts/five_qubit_code/five_qubit_threshold.py
```

### Cirq Fault-Tolerance Tests
- Universal gate validations: `tests/cirq_experiments/support/universal_operations/`
- Fault-tolerant Deutsch-Jozsa algorithm: `tests/cirq_experiments/algorithms/deutsch_josza/test_deutsch_josza.py`

---

## Running Tests

Run the full test suite with `pytest`:

```bash
# Run all fast tests
pytest -m "not slow"

# Run the complete test suite including slow simulation tests
pytest

# Run tests in parallel
pytest -n auto -m "not slow"
```

---

## License

This project is licensed under the [MIT License](LICENSE).
