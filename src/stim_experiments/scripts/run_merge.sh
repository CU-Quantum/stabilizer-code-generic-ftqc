#!/bin/bash

#SBATCH --account=ucb685_asc2
#SBATCH --time=24:00:00
#SBATCH --partition=acpu
#SBATCH --qos=cpu-normal
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --job-name=merge
#SBATCH --error=results/merge/merge_%j.err
#SBATCH --output=results/merge/merge_%j.out
#SBATCH --mail-type=ALL
#SBATCH --mail-user=nipa4599@colorado.edu


# Create and activate a virtual environment
module load anaconda/2023.09
conda env create -f /projects/nipa4599/stim-experiments/environment.yml
conda activate stim-experiments-venv


# Setup workspace
export PYTHONPATH=$PYTHONPATH:/projects/nipa4599/stim-experiments/src
cd /projects/nipa4599/stim-experiments || exit

python /projects/nipa4599/stim-experiments/src/stim_experiments/scripts/merge_results.py

