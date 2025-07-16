#!/bin/bash

#SBATCH --account=ucb685_asc1
#SBATCH --time=01:00:00
#SBATCH --partition=aa100
#SBATCH --nodes=1
#SBATCH --gres=gpu:16
#SBATCH --ntasks=1
#SBATCH --qos=normal
#SBATCH --job-name=deutsch_josza
#SBATCH --error=deutsch_josza_%j.err
#SBATCH --output=deutsch_josza_%j.out
#SBATCH --mail-type=ALL
#SBATCH --mail-user=nipa4599@colorado.edu


# Go to your project directory
cd ~/workspace/stim-experiments


# Create and activate a virtual environment
module load anaconda/2023.09
conda env create -f environment.yml


# Run your scripts
export march=x86_64
apptainer pull nvcr.io/nvidia/cuquantum-appliance:25.03-${march}.sif docker://nvcr.io/nvidia/cuquantum-appliance:25.03-${march}
apptainer run --gpus all \
              --rm nvcr.io/nvidia/cuquantum-appliance:25.03-${march}
              python ~/workspace/stim-experiments/scripts/deutsch_josza_ler_surface_code/deutsch_josza_ler_surface_code.py
