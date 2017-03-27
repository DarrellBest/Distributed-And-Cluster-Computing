#!/bin/sh

sudo apt-get install -y nfs-kernel-server
sudo chmod 777 /home
echo "/home *(rw,sync,no_root_squash)" | sudo tee -a /etc/exports
sudo systemctl restart nfs-kernel-server