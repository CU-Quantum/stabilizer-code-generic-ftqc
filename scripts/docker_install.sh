#!/bin/bash

#SBATCH --account=ucb685_asc1
#SBATCH --time=01:00:00
#SBATCH --partition=aa100
#SBATCH --nodes=1
#SBATCH --gres=gpu:1
#SBATCH --ntasks=1
#SBATCH --qos=normal
#SBATCH --job-name=qsim_setup
#SBATCH --error=qsim_setup_%j.err
#SBATCH --output=qsim_setup_%j.out
#SBATCH --mail-type=ALL
#SBATCH --mail-user=nipa4599@colorado.edu

### DOCKER ###
# Add Docker's official GPG key:
apt-get update
apt-get install ca-certificates curl
install -m 0755 -d /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc
chmod a+r /etc/apt/keyrings/docker.asc

# Add the repository to Apt sources:
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/ubuntu \
  $(. /etc/os-release && echo "${UBUNTU_CODENAME:-$VERSION_CODENAME}") stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
apt-get update

# Install the Docker packages:
apt-get install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin

# Confirm success:
docker run hello-world
