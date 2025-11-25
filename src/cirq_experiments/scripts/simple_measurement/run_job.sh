#!/bin/bash

#SBATCH --account=ucb685_asc1
#SBATCH --time=10:00:00
#SBATCH --partition=amilan
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=10
#SBATCH --qos=normal
#SBATCH --job-name=simple_measurement
#SBATCH --error=results/simple_measurement/simple_measurement_%j.err
#SBATCH --output=results/simple_measurement/simple_measurement_%j.out
#SBATCH --mail-type=ALL
#SBATCH --mail-user=nipa4599@colorado.edu


# Create and activate a virtual environment
module load anaconda/2023.09
conda env create -f /projects/nipa4599/stim-experiments/environment.yml
conda activate stim-experiments-venv


# Setup workspace
export PYTHONPATH=$PYTHONPATH:/projects/nipa4599/stim-experiments/src
cd /projects/nipa4599/stim-experiments


# Run
python /projects/nipa4599/stim-experiments/src/cirq_experiments/scripts/simple_measurement/simple_measurement.py
