# Stabilizer Code-Generic Universal Fault-Tolerant Quantum Computation

A Python framework for fault-tolerant quantum computing (FTQC) and quantum error correction (QEC) experiments across arbitrary stabilizer codes using [Cirq](https://quantumai.google/cirq) and [Stim](https://github.com/quantumlib/Stim).

---

## Overview

This repository provides tools, circuits, and simulation pipelines for:
- **Generic Stabilizer Codes**: Arbitrary stabilizer codes specified by check matrices in standard or non-standard forms (e.g. 5-qubit code, Steane code, Shor code, Dodecacode, Tetrahedral code).
- **Universal Fault-Tolerant Operations**: Ancilla-assisted fault-tolerant logical Clifford + T gates and universal controlled-flip operations.
- **Stim Experiments & Monte Carlo Simulations**: High-performance error threshold and logical error rate simulations using Stim, PyMatching, and LDPC decoders.
- **Cirq State Vector Simulations**: Exact quantum state verification and FTQC algorithm simulations (e.g. Deutsch-Jozsa, logical state preparation, and syndrome extraction).

---

## Repository Structure

```
├── results/                  # Simulation data and results
├── src/
│   ├── cirq_experiments/     # Cirq-based quantum error correction and FTQC framework
│   │   ├── algorithms/       # FTQC algorithm circuits (e.g. Deutsch-Jozsa)
│   │   ├── error_correcting_codes/ # Code implementations (Five-qubit, Steane, Shor, etc.)
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

## Experiments & Benchmarking

Monte Carlo simulations and error threshold benchmarks across stabilizer codes under circuit-level noise using Stim and Sinter.

### Running Code Simulations

Run Stim threshold and logical error rate simulations for different target stabilizer codes:

```bash
# 1. Five-qubit code simulation (with lookup table decoder)
python src/stim_experiments/scripts/five_qubit/five_qubit.py

# 2. Dodecacode [[10, 1, 4]] simulation (with BP-OSD decoder)
python src/stim_experiments/scripts/dodecacode/dodecacode.py

# 3. Generalized Shor Code CX (GSCX) distance 7 simulation (with MWPM decoder)
python src/stim_experiments/scripts/gscx_distance_7/gscx_distance_7.py
```

#### Simulation Options
All simulation scripts accept command-line flags to customize shots, error rates, and multiprocessing:
```bash
python src/stim_experiments/scripts/five_qubit/five_qubit.py \
  --max-shots 1000000 \
  --max-errors 1000 \
  --num-workers 8 \
  --depolarization-probabilities 1e-4 5e-4 0.001 0.005 0.01
```

### Plotting Results

Generate logical error rate (LER) plots from the simulation data:

```bash
# Plot total logical error rate comparison across all codes
python src/stim_experiments/scripts/plot_total_ler.py

# Plot individual code threshold curves
python src/stim_experiments/scripts/plot_qec.py
```

### Cirq Algorithm & Operation Experiments

Verify exact quantum state transformations and run algorithm simulations:

#### 1. Universal Operations Validations
Validate logical $H$, $CX$, and $T$ gate effects:
```bash
# Run all universal operation verification experiments
pytest tests/cirq_experiments/support/universal_operations/

# Or run individual operation test suites:
pytest tests/cirq_experiments/support/universal_operations/universal_hadamard/
pytest tests/cirq_experiments/support/universal_operations/universal_controlled_flip/
pytest tests/cirq_experiments/support/universal_operations/universal_t/
```

#### 2. Deutsch-Jozsa Algorithm
Run Deutsch-Jozsa algorithm experiments with constant and balanced oracles encoded with Generalized Shor codes:
```bash
# Run Deutsch-Jozsa algorithm test suite
pytest tests/cirq_experiments/algorithms/deutsch_josza/
```

---

## Cirq Simulator Guide

For interactive quick-start tutorials, configuration parameters, and custom stabilizer code implementation walkthroughs, see [`cirq_simulator_guide.md`](cirq_simulator_guide.md).

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

## Citation

If you use this repository or framework in your research, please cite:

```bibtex
@misc{papadopoulos2026stabilizercodegenericuniversalfaulttolerant,
      title={Stabilizer Code-Generic Universal Fault-Tolerant Quantum Computation}, 
      author={Nicholas J. C. Papadopoulos and Ramin Ayanzadeh},
      year={2026},
      eprint={2601.10964},
      archivePrefix={arXiv},
      primaryClass={quant-ph},
      url={https://arxiv.org/abs/2601.10964}, 
}
```

---

## License

This project is licensed under the [MIT License](LICENSE).

