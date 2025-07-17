#!/bin/bash

#SBATCH --account=ucb685_asc1
#SBATCH --time=01:00:00
#SBATCH --partition=aa100
#SBATCH --nodes=1
#SBATCH --gres=gpu:3
#SBATCH --ntasks=1
#SBATCH --qos=normal
#SBATCH --job-name=deutsch_josza
#SBATCH --error=deutsch_josza_%j.err
#SBATCH --output=deutsch_josza_%j.out
#SBATCH --mail-type=ALL
#SBATCH --mail-user=nipa4599@colorado.edu


# Create and activate a virtual environment
module load anaconda/2023.09
conda env create -f environment.yml


# Setup workspace
export PYTHONPATH=$PYTHONPATH:~/workspace/stim-experiments/stim-experiments
mkdir -p ~/workspace/stim-experiments/results/deutsch_josza
cd ~/workspace/stim-experiments/results/deutsch_josza


# Run using cuQuantum Appliance
export image_name=nvcr.io/nvidia/cuquantum-appliance:25.03-x86_64
apptainer pull ${image_name}.sif docker://${image_name}
apptainer run --gpus all --rm ${image_name} \
  python ~/workspace/stim-experiments/stim-experiments/scripts/deutsch_josza_ler_surface_code/deutsch_josza_ler_surface_code.py
