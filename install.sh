#!/bin/bash
# Install Script for PAF
# Updates everything
sudo apt-get update -y
sudo apt-get upgrade -y
# Install needed libraries
sudo pip3 install wave
sudo pip3 install argparse
sudo pip3 install matplotlib
sudo pip3 install numpy
sudo pip3 install scipy
sudo pip3 install time
# Download script
wget https://raw.githubusercontent.com/KNFreed/PAF/master/PAF.py