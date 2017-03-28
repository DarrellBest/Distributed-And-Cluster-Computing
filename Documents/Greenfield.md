### Network Topology and Methodology

![alt text](http://i.imgur.com/QxfUvHE.png "Logo Title Text 1")

From https://www.psc.edu/index.php/greenfield:

"Greenfield comprises 360 cores and 18TB of memory in three nodes: two HP DL580s and an HP SuperDome X. Each DL580 contains 4 15-core processors and 3TB of memory. The SuperDome X has 16 15-core processors (for a total of 240 cores) and 12TB of memory."

Our controllerHost acts as an XSEED "node001" for our cluster - the head node. We utilize a database node to reflect the cluster's storage, and 3 slave nodes that act as mirrors of the actual cluster's compute nodes (although there are no hardware differences between the compute nodes themselves).

### Deployment Scripts
This emulated Greenfield infrastructure is deployed with a Python script (through CloudLab's geni-lib library) and several modularized
shell scripts that are used to establish an architecture similar to that of the Greenfield resource:

1) Keyless SSH (for automation)
2) Torque Resource Manager (for job management/scheduling)
3) Network File System (to emulate Greenfield's PSC NFS)
4) Python and OpenMPI (and relevant dependencies)

Notably, however, we chose to deploy our architecture using Ubuntu in lieu of CentOS - largely for ease-of-use.

### Validation Results
