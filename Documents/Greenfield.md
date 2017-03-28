### Network Topology

### Deployment Scripts
This emulated Greenfield infrastructure is deployed with a Python script (through CloudLab's geni-lib library) and several modularized
shell scripts that are used to deploy an architecture similar to that of the Greenfield resource:

1) Keyless SSH (for automation)
2) Torque Resource Manager (for job management/scheduling)
3) Network File System (to emulate Greenfield's Data Supercell)
4) Python and OpenMPI (and relevant dependencies)

Notably, however, we chose to deploy our architecture using Ubuntu instead of CentOS - largely for ease-of-use.

### Validation Results
