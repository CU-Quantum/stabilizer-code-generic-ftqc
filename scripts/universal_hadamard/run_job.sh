#!/bin/bash

#SBATCH --account=ucb685_asc1
#SBATCH --time=10:00:00
#SBATCH --partition=amem
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=10
#SBATCH --qos=normal
#SBATCH --job-name=universal_hadamard
#SBATCH --error=results/universal_hadamard/universal_hadamard_%j.err
#SBATCH --output=results/universal_hadamard/universal_hadamard_%j.out
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
python ~/workspace/stim-experiments/scripts/universal_hadamard/universal_hadamard.py
