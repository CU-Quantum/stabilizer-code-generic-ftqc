#!/bin/bash

#SBATCH --account=ucb685_asc1
#SBATCH --time=01:00:00
#SBATCH --partition=amilan
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --qos=normal
#SBATCH --job-name=deutsch_josza
#SBATCH --error=deutsch_josza_%j.err
#SBATCH --output=deutsch_josza_%j.out
#SBATCH --mail-type=ALL
#SBATCH --mail-user=nipa4599@colorado.edu


# Create and activate a virtual environment
module load anaconda/2023.09
conda env create -f environment.yml
conda activate stim-experiments-venv


# Setup workspace
export PYTHONPATH=$PYTHONPATH:~/workspace/stim_experiments
mkdir -p ~/workspace/stim_experiments/results/deutsch_josza
cd ~/workspace/stim_experiments/results/deutsch_josza


# Run
python ~/workspace/stim_experiments/scripts/deutsch_josza_ler_surface_code/deutsch_josza_ler_surface_code.py
