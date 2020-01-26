#!/bin/bash
# Install Script for PAF
# Updates everything
sudo apt-get update -y
sudo apt-get upgrade -y
sudo apt install python3-pip pkg-config python3-matplotlib python3-scipy -y
# Install needed libraries
pip3 install -r requirements.txt
