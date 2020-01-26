# PAF
PAF - A Python Audio Filter

## 1. Update everything and install Git

```
sudo apt update; apt upgrade -y
sudo apt install git-core
```

## 2. Download the source files and execute the script

```
cd /srv
sudo git clone https://github.com/KNFreed/PAF
sudo chown -R $(whoami): PAF/
cd PAF
chmod a+x install.sh
./install.sh
```
