#!/bin/sh

sudo apt-get install -y nfs-common
sudo mkdir -p /nfs/home
sudo mount 192.168.1.2:/home /nfs/home