#!/bin/bash

# Prepare base system
sudo apt-get update
sudo apt install python3-pip python3-venv
python3 -m venv venv
source venv/bin/activate && pip install wheel && pip install -r requirements/fabric.txt

sudo -H pip3 install pip --upgrade
sudo -H pip3 install wheel
sudo -H pip3 install ansible --upgrade

./fix_ssh.sh