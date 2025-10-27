#!/bin/bash

#SBATCH --account=ucb685_asc1
#SBATCH --time=24:00:00
#SBATCH --partition=amilan
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=10
#SBATCH --qos=normal
#SBATCH --job-name=five_qubit
#SBATCH --error=results/five_qubit/five_qubit%j.err
#SBATCH --output=results/five_qubit/five_qubit%j.out
#SBATCH --mail-type=ALL
#SBATCH --mail-user=nipa4599@colorado.edu


# Create and activate a virtual environment
module load anaconda/2023.09
conda env create -f ~/workspace/stim-experiments/environment.yml
conda activate stim-experiments-venv


# Setup workspace
export PYTHONPATH=$PYTHONPATH:~/workspace/stim-experiments/src
cd ~/workspace/stim-experiments


# Run
python ~/workspace/stim-experiments/src/stim_experiments/scripts/five_qubit/five_qubit.py -s 10_000_000_000 -e 100_00 -p 1e-6 5e-6 1e-5 5e-5 1e-4 5e-4 1e-3 5e-3 1e-2
