#!/bin/sh

sudo wget https://www.open-mpi.org/software/ompi/v1.10/downloads/openmpi-1.10.3.tar.gz
sudo apt-get install libibnetdisc-dev
tar -xvf openmpi-1.10.3.tar.gz
cd openmpi-1.10.3
./configure --prefix="/software/openmpi/1.10.3"
sudo make
sudo make install

#Configuration
#sudo nano /etc/environment
#Edit the environment file so that it contains the following lines:
#PATH=$PATH:/software/openmpi/1.10.3/bin"
#LD_LIBRARY_PATH="$LD_LIBRARY_PATH:/software/openmpi/1.10.3//lib/"7.
