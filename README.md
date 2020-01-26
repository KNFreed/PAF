# PAF
PAF - A Python Audio Filter

## 1. Update everything and install Git

```
sudo apt update; apt upgrade -y
sudo apt install git-core
```

## 2. Download the source files and execute the script

```
sudo git clone https://github.com/KNFreed/PAF
sudo chown -R $(whoami): PAF/
cd PAF
chmod a+x install.sh
./install.sh
```

## 3. How to use

```
python3 PAF.py [IMPUT FILE] -filter -flags
```
List of all filters : 
"-l", "--lowpass": Low pass filter. Default value: 5000.
"-hi", "--highpass":High pass filter. Default value: 5000.
"-bp", "--bandpass": Band pass filter. Default value: 5000 10000.
"-bs", "--bandstop": Band Stop filter. Default value: 5000 10000.
Available flags :
"-o", "--output": Name of the output wav file. Default value: output.wav.
"-s", "--sampling": Sampling rate. Default value: same as input.
