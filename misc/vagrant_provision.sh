#!/bin/bash
sudo apt-get update
sudo apt-get install -y python-pip  python-dev
sudo -H pip install -r /vagrant/misc/requirements.txt

cd /vagrant
ansible-playbook configure_servers.yml --extra-vars '@variables/local.yml' -i 'localhost,' --connection local
