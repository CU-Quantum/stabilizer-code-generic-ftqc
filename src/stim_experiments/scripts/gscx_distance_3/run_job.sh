#!/bin/bash

#SBATCH --account=ucb685_asc2
#SBATCH --time=24:00:00
#SBATCH --array=0-9
#SBATCH --partition=amem
#SBATCH --qos=mem-normal
#SBATCH --mem=512G
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --job-name=gsc_d3
#SBATCH --error=results/gscx_distance_3/gscx_distance_3_%j.err
#SBATCH --output=results/gscx_distance_3/gscx_distance_3_%j.out
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
python /projects/nipa4599/stim-experiments/src/stim_experiments/scripts/gscx_distance_3/gscx_distance_3.py \
  -s 100_000_000 \
  -e 500 \
  -p 2e-4 5e-4 1e-3 2e-3 5e-3 1e-2 2e-2 5e-2 1e-1 2e-1 5e-1
