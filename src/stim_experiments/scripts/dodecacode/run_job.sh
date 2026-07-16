#!/bin/bash

#SBATCH --account=ucb685_asc1
#SBATCH --time=24:00:00
#SBATCH --array=0-999
#SBATCH --partition=amem
#SBATCH --qos=mem
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --mem=512G
#SBATCH --job-name=dodecacode
#SBATCH --error=results/dodecacode/dodecacode_%j.err
#SBATCH --output=results/dodecacode/dodecacode_%j.out
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
python /projects/nipa4599/stim-experiments/src/stim_experiments/scripts/dodecacode/dodecacode.py \
  -s 1_000_000_000 \
  -e 500 \
  -p 5e-5 1e-4 2e-4 5e-4 1e-3 2e-3 5e-3 1e-2 2e-2 5e-2 1e-1 2e-1 5e-1 \
  -d exact_mw
