#!/bin/bash

#SBATCH --account=ucb685_asc1
#SBATCH --time=24:00:00
#SBATCH --array=0-999
#SBATCH --partition=amilan
#SBATCH --qos=normal
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --job-name=five_qubit
#SBATCH --error=results/five_qubit/five_qubit_%j.err
#SBATCH --output=results/five_qubit/five_qubit_%j.out
#SBATCH --mail-type=ALL
#SBATCH --mail-user=nipa4599@colorado.edu


# Create and activate a virtual environment
module load anaconda/2023.09
conda env create -f /projects/nipa4599/stim-experiments/environment.yml
conda activate stim-experiments-venv


# Setup workspace
export PYTHONPATH=$PYTHONPATH:/projects/nipa4599/stim-experiments/src
cd /projects/nipa4599/stim-experiments || exit


# Run
python /projects/nipa4599/stim-experiments/src/stim_experiments/scripts/five_qubit/five_qubit.py \
  -s 1_000_000_000 \
  -e 10_000 \
  -p 1e-6 5e-6 1e-5 5e-5 1e-4 5e-4 1e-3 5e-3 1e-2
