#!/bin/bash

#SBATCH --account=ucb-general
#SBATCH --time=01:00:00
#SBATCH --partition=amilan
#SBATCH --nodes=1
#SBATCH --job-name=deutsch_josza
#SBATCH --error=deutsch_josza_%j.err
#SBATCH --output=deutsch_josza_%j.out
#SBATCH --mail-type=ALL
#SBATCH --mail-user=nipa4599@colorado.edu



# Go to your project directory
cd ~/workspace/stim-experiments


# Create and activate a virtual environment
module load anaconda/2023.09
#conda create -n stim-experiments python=3.12
conda activate stim-experiments


# Install required packages
conda env create -f environment.yaml


# Run your scripts
python3 src/download_fma.py

python3 src/process_fma.py

python3 src/train.py

python3 src/test.py
