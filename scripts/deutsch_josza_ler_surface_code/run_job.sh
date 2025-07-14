#!/bin/bash

#SBATCH --account=ucb685_asc1
#SBATCH --time=01:00:00
#SBATCH --partition=aa100
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
EXPORT march=x86_64
docker pull nvcr.io/nvidia/cuquantum-appliance:25.03-${march}
docker run --gpus all \
           --rm nvcr.io/nvidia/cuquantum-appliance:25.03-${march}
           python ~/workspace/stim-experiments/scripts/deutsch_josza_ler_surface_code/deutsch_josza_ler_surface_code.py
