#!/bin/bash
# Install Script for PAF
# Updates everything
sudo apt-get update -y
sudo apt-get upgrade -y
# Install needed libraries
$1/bin/pip install -r requirements.txt
