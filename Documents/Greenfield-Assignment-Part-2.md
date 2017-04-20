###### Group 2 - Greenfield: Steven Nix, Darrell Best, Earl Honeycutt



### Network Topology and Methodology

![alt text](http://i.imgur.com/QxfUvHE.png "Logo Title Text 1")

From https://www.psc.edu/index.php/greenfield:

"Greenfield comprises 360 cores and 18TB of memory in three nodes: two HP DL580s and an HP SuperDome X. Each DL580 contains 4 15-core processors and 3TB of memory. The SuperDome X has 16 15-core processors (for a total of 240 cores) and 12TB of memory."

Our controllerHost node acts as an XSEDE "node001" for our cluster - the head node. We utilize a database node to reflect the cluster's storage, and 3 slave nodes that act as mirrors of the actual cluster's computer nodes (although we do not perfectly replicate the hardware present in the Greenfield worker nodes). Our cluster nodes and controller/database nodes are all connected through an ethernet LAN interface. 



### Deployment Script
This emulated Greenfield infrastructure is deployed with a Python script that instantiates the network topology described above using CloudLab's geni-lib. While Greenfield operates on CentOS, we chose to deploy our architecture using Ubuntu-16.04 in lieu of CentOS66 - largely for ease-of-use and setup on our end. Listed below are the additional features deployed through our script. There also is a lack of documentation on what they used in lieu of NFS so we went ahead and used NFS.

First our script deploys a network file system with the aim of allowing the head node and the slave nodes to communicate through file sharing over LAN. An NFS server is installed on the database node and NFS clients are installed on all other nodes. Once the NFS is established, shared directories are mounted and utilized for sharing elements like programs in the packages folder and the local home directory. Afterwards, other relevant applications are installed through apt-get (or downloaded for installation with wget) and started/restarted for proper initialization.  

Listed below are implemented functionalities:

1) Torque Resource Manager (for job management/scheduling)
2) A Network File System (to emulate Greenfield's PSC NFS)
4) environment-modules (http://modules.sourceforge.net/)
3) Python and OpenMPI and relevant dependencies (2.7.13, 2.1.0)
4) gcc (6.3.0)

This Code could be much more compact however due to lack of knowledge in the begining we kept the script like this.
For these sections below please see the script file for more comments detailing the installation process.
I have provided line numbers to make it easier to analyse the script however they may not exactly line up.
This script was built off of https://github.com/clemsonbds/hpccsystems/blob/master/hpccsystems.py but aside for Pre-Initialization
and parts of Initialization most of it is our work.

Pre-Initialization (lines 1-32): 
	This section of code sets up the cloudlab initalization gui for users when they are making the experiment. It allows users to set variables like names and number of nodes before
	the experiment starts. It also provides a description and a basic set of instructions. Unfortunately the number of nodes must be 3 due to Torque setup.

Initialization (lines 33-66):
	This section of code is where the basic topolgy is setup. It creates a LAN, initializes barebone pc's with Ubuntu-16.04, names them based on user input from the previous section, and sets up the network configurations. It also sets up dependiencies that are required later on that are needed on every node (python-pip, python-setuptools, mpich).

Backbone Program Installations (lines 68-206):
	This section of code sets up the programs that make this group of computers a cluster. These programs are NFS, Torque, and environment-modules. 
	
	NFS (lines 68-105): 
		This section sets up the database node and the rest of the nodes to share /packages and /home from the database to /nfs/home and /nfs/packages on the rest of the nodes. /nfs/home is the home directory of database however every node is setup with cloudlabs /users folder meaning it is the home for non cloudlab made accounts (sudo adduser accounts). 

	Torque (lines 106-203): 
		This section sets up Torque with controllerHost being the server and node2, node3, and node4 being clients excluding the database node. ControllerHost is the only node capable of submitting jobs. Right now the worker nodes are setup to utilize 50 cores per node out of 56. The clients are also setup to take advantage of the /nfs/home directory and thus torque mom is setup to copy job output
		files such as *.o and *.e files into the /nfs/.. directory they were ran from.

	Enviornment-Modules (lines 204-274):
		This section sets up enviornment-modules which allows for programs to be installed to the database and then loaded, removed, swithced, etc by giving each program its own enviornment. This program is used to load up lesser progrmas such as python, gcc, and openmpi. Also since I can install them all to the database node and mount them with this method, only the database node needs to be kept up to date. Finally since I can install and run several different versions of each program compatibility issues decrease.

Lesser Program Installation (lines 208-276):
	This section of code sets up GCC, Python, and OpenMPI. GCC is needed to build the other two lesser programs plus just about any other program. Python is needed for python applications and libraries such as mpi4py. OpenMPI is used to allow communication between the nodes. Unfortunately openMPI needs passwordless-ssh setup in order to work so it doesn't work as of right now.



### Validation Results

1) NFS:	
	NFS is fully implemented and mounts from the Database node to all other nodes. The mounted directories are database: /home and /packages and mounts them to the other nodes in the /nfs/home and 
	/nfs/packages.

2) Torque(PBS): 
	Torque is fully implemented. It allows users to queue jobs including interactive and also successfully returns the jobs output files automatically to the directory the job is ran from.

3) Environment-Modules:
	EM is fully implemented. It is completely configured and allows admins to add programs into it for use using module add. As of right now GCC, Python, and OpenMPI are installed and do work as far as EM is concerned however OpenMPI is having other non-related issues.

4) Passwordless-SSH:
	Passwordless-SSH is NOT implemented. There have been multiple attempts to setup Passwordless-ssh but due to the way the home and users directories are setup these attempts resulted in failure. We have found successfully set up passwordless-ssh manually but unfortunately don't have enough time to add it into the script and test it. Due to this openMPI won't work.

5) Python, GCC, OpenMPI:
	-Python is installed and implemented.
	-GCC is installed and implemented.
	-OpenMPI is installed and implemented, but cannot be completely verifed due to issues with passwordless-ssh.



### Notes

Unfortunately I made some changes to the Script and I can't get pictures of the validation right now until it comes completely up.