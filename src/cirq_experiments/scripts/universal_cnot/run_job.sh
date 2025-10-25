#!/bin/bash

#SBATCH --account=ucb685_asc1
#SBATCH --time=24:00:00
#SBATCH --partition=amem
#SBATCH --nodes=4
#SBATCH --ntasks=8
#SBATCH --cpus-per-task=16
#SBATCH --qos=mem
#SBATCH --job-name=universal_cnot
#SBATCH --error=results/universal_cnot/universal_cnot_%j.err
#SBATCH --output=results/universal_cnot/universal_cnot_%j.out
#SBATCH --mail-type=ALL
#SBATCH --mail-user=nipa4599@colorado.edu


# Create and activate a virtual environment
module load anaconda/2023.09
conda env create -f ~/workspace/stim-experiments/environment.yml
conda activate stim-experiments-venv


# Setup workspace
export PYTHONPATH=$PYTHONPATH:~/workspace/stim-experiments
cd ~/workspace/stim-experiments


# Run
python ~/workspace/stim-experiments/src/cirq_experiments/scripts/universal_cnot/universal_cnot.py
