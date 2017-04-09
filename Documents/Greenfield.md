###### Group 2 - Greenfield: Steven Nix, Darrell Best, Earl Honeycutt

### Network Topology and Methodology

![alt text](http://i.imgur.com/QxfUvHE.png "Logo Title Text 1")

From https://www.psc.edu/index.php/greenfield:

"Greenfield comprises 360 cores and 18TB of memory in three nodes: two HP DL580s and an HP SuperDome X. Each DL580 contains 4 15-core processors and 3TB of memory. The SuperDome X has 16 15-core processors (for a total of 240 cores) and 12TB of memory."

Our controllerHost node acts as an XSEDE "node001" for our cluster - the head node. We utilize a database node to reflect the cluster's storage, and 3 slave nodes that act as mirrors of the actual cluster's compute nodes (although we do not perfectly replicate the hardware present in the Greenfield worker nodes). Our cluster nodes and controller/database nodes are all connected through an ethernet LAN interface and utilize keyless SSH ("Use SSH to connect to greenfield.psc.xsede.org. SSH is a program that enables secure logins over an unsecure network.").

### Deployment Script
This emulated Greenfield infrastructure is deployed with a Python script that instantiates the network topology described above using CloudLab's geni-lib. While Greenfield operates on CentOS, we chose to deploy our architecture using Ubuntu16 in lieu of CentOS66 - largely for ease-of-use and setup on our end. Listed below are the additional features deployed through our script.

1) Keyless SSH
2) Torque Resource Manager (for job management/scheduling)
3) A Network File System (to emulate Greenfield's PSC NFS)
4) Python and OpenMPI (and relevant dependencies, including gcc)

### Validation Results