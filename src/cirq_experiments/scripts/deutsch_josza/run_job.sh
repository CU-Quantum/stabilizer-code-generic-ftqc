#!/bin/bash

#SBATCH --account=ucb685_asc1
#SBATCH --time=01:00:00
#SBATCH --partition=amilan
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --qos=normal
#SBATCH --job-name=deutsch_josza
#SBATCH --error=results/deutsch_josza/deutsch_josza_%j.err
#SBATCH --output=results/deutsch_josza/deutsch_josza_%j.out
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
python ~/workspace/stim-experiments/src/cirq_experiments/scripts/deutsch_joszae/deutsch_josza.py
