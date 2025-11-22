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
conda env create -f /scratch/alpine/nipa4599/stim-experiments/environment.yml
conda activate stim-experiments-venv


# Setup workspace
export PYTHONPATH=$PYTHONPATH:/scratch/alpine/nipa4599/stim-experiments/src
cd /scratch/alpine/nipa4599/stim-experiments


# Run
python /scratch/alpine/nipa4599/stim-experiments/src/cirq_experiments/scripts/deutsch_joszae/deutsch_josza.py
