from stim import Circuit
from stim_experiments import SurfaceCodeStim
from stim_experiments.surface_code import LatticeSurgery
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt
import os
from datetime import datetime

def print_measurement_table(samples):
    """Print measurement results in a formatted table"""
    print("\nFirst 10 Measurement Results:")
    print(f"{'Shot':4s} | {'Oracle M1':9s} | {'Debug M0':8s} | {'Debug M1':8s} | {'Final M0':8s}")
    print("-" * 50)
    for i, shot in enumerate(samples):
        print(f"{i+1:4d} | {int(shot[0]):9d} | {int(shot[1]):8d} | {int(shot[2]):8d} | {int(shot[3]):8d}")

def visualize_results(samples, shots):
    """Visualize measurement results and correlations"""
    # Create figure with two subplots
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 5))
    
    # Plot measurement probabilities
    labels = ['Oracle M1', 'Debug M0', 'Debug M1', 'Final M0']
    probabilities = [sum(samples[:, i])/shots * 100 for i in range(4)]
    
    ax1.bar(labels, probabilities)
    ax1.set_ylabel('Percentage of ones (%)')
    ax1.set_title('Measurement Probabilities')
    ax1.tick_params(axis='x', rotation=45)
    
    # Plot correlation matrix
    corr_matrix = np.zeros((4, 4))
    for i in range(4):
        for j in range(4):
            corr_matrix[i, j] = sum(samples[:, i] == samples[:, j])/shots
    
    im = ax2.imshow(corr_matrix, cmap='coolwarm', vmin=0, vmax=1)
    ax2.set_xticks(range(4))
    ax2.set_yticks(range(4))
    ax2.set_xticklabels(labels, rotation=45)
    ax2.set_yticklabels(labels)
    ax2.set_title('Measurement Correlations')
    plt.colorbar(im, ax=ax2)
    
    plt.tight_layout()
    return fig

def analyze_results(samples, shots=1000, confidence=0.95):
    """Analyze measurement results with confidence intervals"""
    measurements = {
        'Oracle M1': samples[:, 0],
        'Debug M0': samples[:, 1],
        'Debug M1': samples[:, 2],
        'Final M0': samples[:, 3]
    }
    
    print("\nDetailed Statistics with Confidence Intervals:")
    print("-" * 60)
    print(f"Total shots: {shots}")
    
    for name, data in measurements.items():
        ones = sum(data)
        p = ones/shots
        if p == 0 or p == 1:
            # Handle edge cases where p is 0 or 1
            ci = (p, p)
            ci_str = f"{p*100:.1f}%"
        else:
            # Calculate confidence interval
            ci = stats.norm.interval(confidence, loc=p, scale=np.sqrt(p*(1-p)/shots))
            ci_str = f"[{ci[0]*100:.1f}%, {ci[1]*100:.1f}%]"
        
        print(f"{name:8s}: {ones}/{shots} ({p*100:.1f}% ones)")
        print(f"          {confidence*100}% CI: {ci_str}")
    
    # Correlation analysis
    correlations = samples[:, 1] == samples[:, 3]  # Debug M0 vs Final M0
    corr_rate = sum(correlations)/shots
    print(f"\nCorrelation Analysis:")
    print(f"Debug M0 vs Final M0: {corr_rate*100:.1f}% match")

def run_1qubit_simons_with_lattice_surgery() -> Circuit:
    """
    Constructs the full circuit for 1-qubit Simon's Algorithm
    using surface code logical patches and lattice surgery to implement
    a logical CNOT-based oracle (Uf).
    Returns the full Stim circuit.
    """

    # Step 1: Create logical input and output patches
    circuit_input = Circuit("H 0")     # Input qubit in |+>
    circuit_output = Circuit("")       # Output qubit in |0>

    input_patch = SurfaceCodeStim(circuit_input)
    output_patch = SurfaceCodeStim(circuit_output)

    # Step 2: Perform logical CNOT via lattice surgery (oracle)
    surgery = LatticeSurgery(input_patch, output_patch)
    full_circuit = surgery.logical_cnot()
    
    # Debug: Measure qubits after the oracle
    full_circuit.append_operation("M", [0])
    full_circuit.append_operation("M", [1])
    full_circuit.append_from_stim_program_text("TICK")
    
    # Step 3: Apply Hadamard to input after oracle
    full_circuit.append_operation("H", [0])
    full_circuit.append_from_stim_program_text("TICK")
    
    # Step 4: Measure the input qubit to get 's'
    full_circuit.append_operation("M", [0])
    full_circuit.append_from_stim_program_text("TICK")

    return full_circuit

def main():
    """Main function to run Simon's algorithm and analyze results"""
    # Experiment configuration
    shots = 1000
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_dir = "results"
    
    # Create results directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    # Generate and display circuit
    circuit = run_1qubit_simons_with_lattice_surgery()
    print("Circuit:")
    print(circuit)

    # Sample measurements
    samples = circuit.compile_sampler().sample(shots=shots)

    # Display first 10 shots in table format
    print_measurement_table(samples[:10])

    # Analyze results
    analyze_results(samples, shots=shots)
    
    # Visualize results
    fig = visualize_results(samples, shots)
    
    # Save results with timestamp
    output_file = f"{output_dir}/simons_algorithm_results_{timestamp}"
    plt.savefig(f"{output_file}.png", dpi=300, bbox_inches='tight')
    plt.close()
    
    # Save raw data
    np.save(f"{output_file}_data.npy", samples)
    
    print(f"\nResults saved to {output_dir}/")

if __name__ == "__main__":
    main()
