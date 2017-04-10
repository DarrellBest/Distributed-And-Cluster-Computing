import geni.portal as portal
import geni.rspec.pg as rspec
import geni.rspec.igext as IG

pc = portal.Context()
request = rspec.Request()

pc.defineParameter("workerCount",
					"Number of Greenfield slaves",
					portal.ParameterType.INTEGER, 3)

pc.defineParameter("controllerHost", "Name of controller node",
					portal.ParameterType.STRING, "controllerHost", advanced=True,
					longDescription="The short name of the controller node.	You shold leave this alone unless you really want the hostname to change.")
					
pc.defineParameter("database", "Name of datbase",
					portal.ParameterType.STRING, "database", advanced=True,
					longDescription="The short name of the controller node.	You shold leave this alone unless you really want the hostname to change.")
					
params = pc.bindParameters()

tourDescription = "This profile is based off of the Greenfield Cluster with some changes to make it more compatible with Cloudlab."

tourInstructions = \
	"""
### Basic Instructions
Once your experiment nodes have booted, and this profile's configuration scripts have finished deploying HPCCSystems inside your experiment, you'll be able to visit [the ECLWatch interface](http://{host-%s}:8010) (approx. 5-15 minutes).  
""" % (params.controllerHost)

#
# Setup the Tour info with the above description and instructions.
#	
tour = IG.Tour()
tour.Description(IG.Tour.TEXT,tourDescription)
tour.Instructions(IG.Tour.MARKDOWN,tourInstructions)
request.addTour(tour)


# Create a Request object to start building the RSpec.
#request = portal.context.makeRequestRSpec()
#request 
# Create a link with type LAN
link = request.LAN("lan")

# Generate the nodes
for i in range(params.workerCount + 2):
	if i == 0:
		node = request.RawPC(params.controllerHost)
	elif i == 1:
		node = request.RawPC(params.database)
	else:
		node = request.RawPC("node" + str(i))
	
	node.disk_image = "urn:publicid:IDN+emulab.net+image+emulab-ops:UBUNTU16-64-STD"
	iface = node.addInterface("if" + str(i))
	iface.component_id = "eth1"
	iface.addAddress(rspec.IPv4Address("192.168.1." + str(i + 1), "255.255.255.0"))
	link.addInterface(iface)
	
	node.addService(rspec.Execute(shell="/bin/sh",
									command="sudo adduser --ingroup adm --disabled-password greenfield"))
	node.addService(rspec.Execute(shell="/bin/sh",
									command="sudo adduser greenfield sudo"))
	node.addService(rspec.Execute(shell="/bin/sh",
									command="sudo apt-get update"))
	node.addService(rspec.Execute(shell="/bin/sh",
									command="sudo apt-get install -y python-setuptools python-pip"))
	node.addService(rspec.Execute(shell="/bin/sh",
									command="sudo apt-get install -y mpich"))
	if i == 1:
		# install nfs server
		node.addService(rspec.Execute(shell="/bin/sh",
								command="sudo apt-get install -y nfs-kernel-server"))
		node.addService(rspec.Execute(shell="/bin/sh",
								command="sudo chmod 777 /home"))
		node.addService(rspec.Execute(shell="/bin/sh",
								command="echo '/home *(rw,sync,no_root_squash)' | sudo tee -a /etc/exports"))
		node.addService(rspec.Execute(shell="/bin/sh",
								command="sudo mkdir /packages"))
		node.addService(rspec.Execute(shell="/bin/sh",
								command="sudo chmod 777 /packages"))
		node.addService(rspec.Execute(shell="/bin/sh",
								command="echo '/packages *(rw,sync,no_root_squash)' | sudo tee -a /etc/exports"))			
		node.addService(rspec.Execute(shell="/bin/sh",
								command="sudo systemctl restart nfs-kernel-server"))
		node.addService(rspec.Execute(shell="/bin/sh",
								command="mkdir /home/.ssh"))								
		node.addService(rspec.Execute(shell="/bin/sh",
								command="ssh-keygen -t rsa -P '' -f '/home/.ssh/id_rsa' "))
		node.addService(rspec.Execute(shell="/bin/sh",
								command="sudo chmod 777 /home/.ssh"))		
		node.addService(rspec.Execute(shell="/bin/sh",
								command="cp /home/.ssh/id_rsa.pub /home/.ssh/authorized_keys"))
	else:
	# install nfs client
		node.addService(rspec.Execute(shell="/bin/sh",
								command="sudo apt-get install -y nfs-common"))
		node.addService(rspec.Execute(shell="/bin/sh",
								command="sudo mkdir -p /nfs/home"))
		node.addService(rspec.Execute(shell="/bin/sh",
								command="sudo mkdir -p /nfs/packages"))
		node.addService(rspec.Execute(shell="/bin/sh",
								command="sudo mount 192.168.1.2:/home /nfs/home"))
		node.addService(rspec.Execute(shell="/bin/sh",
								command="sudo mount 192.168.1.2:/packages /nfs/packages"))
													
	if i == 0:
		#must be in root to install torque
		#node.addService(rspec.Execute(shell="/bin/sh",
		#						command="sudo su"))
		#apt-get install torque
		node.addService(rspec.Execute(shell="/bin/sh",
								command="sudo apt-get install -y torque-server torque-client torque-mom torque-pam"))
		#stop the default torque server
		node.addService(rspec.Execute(shell="/bin/sh",
								command="sudo service torque-mom stop"))
		node.addService(rspec.Execute(shell="/bin/sh",
								command="sudo service torque-scheduler stop"))
		node.addService(rspec.Execute(shell="/bin/sh",
								command="sudo service torque-server stop"))
		#create custom torque server
		node.addService(rspec.Execute(shell="/bin/sh",
								command="yes | pbs_server -t create"))
		#kill custom torque server
		node.addService(rspec.Execute(shell="/bin/sh",
								command="sudo killall pbs_server"))		
		#configure torque server
		node.addService(rspec.Execute(shell="/bin/sh",
								command="echo 'controllerHost-lan' | sudo tee /etc/torque/server_name"))
		node.addService(rspec.Execute(shell="/bin/sh",
								command="echo 'controllerHost-lan' | sudo tee /var/spool/torque/server_priv/acl_svr/acl_hosts"))
		node.addService(rspec.Execute(shell="/bin/sh",
								command="echo 'root@controllerHost-lan' | sudo tee -a /var/spool/torque/server_priv/acl_svr/operators"))
		node.addService(rspec.Execute(shell="/bin/sh",
								command="echo 'root@controllerHost-lan' | sudo tee -a /var/spool/torque/server_priv/acl_svr/managers"))
							
		
		#add work nodes to server
		node.addService(rspec.Execute(shell="/bin/sh",
								command="echo 'node2 np=50' | sudo tee /var/spool/torque/server_priv/nodes"))		
		node.addService(rspec.Execute(shell="/bin/sh",
								command="echo 'node3 np=50' | sudo tee -a /var/spool/torque/server_priv/nodes"))
		node.addService(rspec.Execute(shell="/bin/sh",
								command="echo 'node4 np=50' | sudo tee -a /var/spool/torque/server_priv/nodes"))								
		#configure mom
		node.addService(rspec.Execute(shell="/bin/sh",
								command="echo 'root@controllerHost-lan' | sudo tee -a /var/spool/torque/mom_priv/config"))
		node.addService(rspec.Execute(shell="/bin/sh",
								command="echo '\$usecp *:/nfs/home /nfs/home' | sudo tee -a /var/spool/torque/mom_priv/config"))
		#start torque
		node.addService(rspec.Execute(shell="/bin/sh",
								command="sudo service torque-mom start"))
		node.addService(rspec.Execute(shell="/bin/sh",
								command="sudo service torque-scheduler start"))
		node.addService(rspec.Execute(shell="/bin/sh",
								command="sudo service torque-server start"))	
		node.addService(rspec.Execute(shell="/bin/sh",
								command="sudo pbs_server"))	
		
		#set scheduling properties
		node.addService(rspec.Execute(shell="/bin/sh",
								command="sudo qmgr -c 'set server scheduling = True'"))
		node.addService(rspec.Execute(shell="/bin/sh",
								command="sudo qmgr -c 'set server keep_completed = 300'"))
		node.addService(rspec.Execute(shell="/bin/sh",
								command="sudo qmgr -c 'set server mom_job_sync = True'"))
		#create default queue
		node.addService(rspec.Execute(shell="/bin/sh",
								command="sudo qmgr -c 'create queue batch'"))
		node.addService(rspec.Execute(shell="/bin/sh",
								command="sudo qmgr -c 'set queue batch queue_type = execution'"))
		node.addService(rspec.Execute(shell="/bin/sh",
								command="sudo qmgr -c 'set queue batch started = true'"))
		node.addService(rspec.Execute(shell="/bin/sh",
								command="sudo qmgr -c 'set queue batch enabled = true'"))
		node.addService(rspec.Execute(shell="/bin/sh",
								command="sudo qmgr -c 'set queue batch resources_default.walltime = 1:00:00'"))
		node.addService(rspec.Execute(shell="/bin/sh",
								command="sudo qmgr -c 'set queue batch resources_default.nodes = 1'"))
		node.addService(rspec.Execute(shell="/bin/sh",
								command="sudo qmgr -c 'set server default_queue = batch'"))	
		#configure submission pool
		node.addService(rspec.Execute(shell="/bin/sh",
								command="sudo qmgr -c 'set server submit_hosts = controllerHost-lan'"))
		node.addService(rspec.Execute(shell="/bin/sh",
								command="sudo qmgr -c 'set server allow_node_submit = true'"))
	
	elif i != 1 and i != 0:	
		#apt-get install torque
		node.addService(rspec.Execute(shell="/bin/sh",
								command="sudo apt-get install -y torque-client torque-mom"))
		#stop torque-mom
		node.addService(rspec.Execute(shell="/bin/sh",
								command="sudo service torque-mom stop"))
		#copy output to shared directory
		node.addService(rspec.Execute(shell="/bin/sh",
								command="echo '\$usecp *:$PWD $PWD' | sudo tee -a /var/spool/torque/mom_priv/config"))
		#point client to server
		node.addService(rspec.Execute(shell="/bin/sh",
								command="echo 'controllerHost-lan' | sudo tee /etc/torque/server_name"))
		#start torque-mom
		node.addService(rspec.Execute(shell="/bin/sh",
								command="sudo service torque-mom start"))
	#install enviornment modules
	node.addService(rspec.Execute(shell="/bin/sh",
							command="sudo apt-get install -y environment-modules"))

	#install programs to modules 
	if i == 1:
		#gcc
		node.addService(rspec.Execute(shell="/bin/sh",
								command="wget -P /packages/gcc/ mirrors-usa.go-parts.com/gcc/releases/gcc-6.3.0/gcc-6.3.0.tar.gz"))	
		node.addService(rspec.Execute(shell="/bin/sh",
								command="mkdir /packages/gcc/6.3.0"))									
		node.addService(rspec.Execute(shell="/bin/sh",
								command="tar -C /packages/gcc/ -xvf  /packages/gcc/gcc-6.3.0.tar.gz"))
		node.addService(rspec.Execute(shell="/bin/sh",
								command="sudo apt-get install -y libc6:i386 libstdc++6:i386"))
		node.addService(rspec.Execute(shell="/bin/sh",
								command="sudo apt-get install -y libmpc-dev"))
		node.addService(rspec.Execute(shell="/bin/sh",
								command="cd /packages/gcc/6.3.0 ; /packages/gcc/gcc-6.3.0/configure --prefix=/packages/gcc/6.3.0 --disable-multilib"))
		node.addService(rspec.Execute(shell="/bin/sh",
								command="cd /packages/gcc/6.3.0 ; make ; make install"))
		
		#python
		node.addService(rspec.Execute(shell="/bin/sh",
								command="wget -P /packages/python/ https://www.python.org/ftp/python/2.7.13/Python-2.7.13.tgz"))	
		node.addService(rspec.Execute(shell="/bin/sh",
								command="mkdir /packages/python/2.7.13"))									
		node.addService(rspec.Execute(shell="/bin/sh",
								command="tar -C /packages/python/ -xvf  /packages/python/Python-2.7.13.tgz"))
		node.addService(rspec.Execute(shell="/bin/sh",
								command="cd /packages/python/2.7.13 ; /packages/python/Python-2.7.13/configure --prefix=/packages/python/2.7.13"))
		node.addService(rspec.Execute(shell="/bin/sh",
								command="cd /packages/python/2.7.13 ; make ; make install"))
		
		#openmpi
		node.addService(rspec.Execute(shell="/bin/sh",
								command="wget -P /packages/openmpi/ https://www.open-mpi.org/software/ompi/v2.1/downloads/openmpi-2.1.0.tar.gz"))	
		node.addService(rspec.Execute(shell="/bin/sh",
								command="mkdir /packages/openmpi/2.1.0"))									
		node.addService(rspec.Execute(shell="/bin/sh",
								command="tar -C /packages/openmpi/ -xvf  /packages/openmpi/openmpi-2.1.0.tar.gz"))
		node.addService(rspec.Execute(shell="/bin/sh",
								command="cd /packages/openmpi/2.1.0 ; /packages/openmpi/openmpi-2.1.0/configure --prefix=/packages/openmpi/2.1.0"))
		node.addService(rspec.Execute(shell="/bin/sh",
								command="cd /packages/openmpi/2.1.0 ; make ; make install"))		

								
	#install module files
	if i == 1 :
		#gcc
		node.addService(rspec.Execute(shell="/bin/sh",
						command="cd /usr/share/modules/modulefiles/ ; sudo mkdir gcc ; cd gcc ; sudo wget https://raw.githubusercontent.com/DarrellBest/Distributed-And-Cluster-Computing/master/Cloudlab_Scripts/gcc_db/6.3.0 "))
		#python
		node.addService(rspec.Execute(shell="/bin/sh",
						command="cd /usr/share/modules/modulefiles/ ; sudo mkdir python ; cd python ; sudo wget https://raw.githubusercontent.com/DarrellBest/Distributed-And-Cluster-Computing/master/Cloudlab_Scripts/python_db/2.7.13 "))
		#openmpi
		node.addService(rspec.Execute(shell="/bin/sh",
						command="cd /usr/share/modules/modulefiles/ ; sudo mkdir openmpi ; cd openmpi ; sudo wget https://raw.githubusercontent.com/DarrellBest/Distributed-And-Cluster-Computing/master/Cloudlab_Scripts/openmpi_db/2.1.0 "))							
	else:
		#gcc
		node.addService(rspec.Execute(shell="/bin/sh",
						command="cd /usr/share/modules/modulefiles/ ; sudo mkdir gcc ; cd gcc ; sudo wget https://raw.githubusercontent.com/DarrellBest/Distributed-And-Cluster-Computing/master/Cloudlab_Scripts/gcc_node/6.3.0 "))
		#python
		node.addService(rspec.Execute(shell="/bin/sh",
						command="cd /usr/share/modules/modulefiles/ ; sudo mkdir python ; cd python ; sudo wget https://raw.githubusercontent.com/DarrellBest/Distributed-And-Cluster-Computing/master/Cloudlab_Scripts/python_node/2.7.13 "))
		#openmpi
		node.addService(rspec.Execute(shell="/bin/sh",
						command="cd /usr/share/modules/modulefiles/ ; sudo mkdir openmpi ; cd openmpi ; sudo wget https://raw.githubusercontent.com/DarrellBest/Distributed-And-Cluster-Computing/master/Cloudlab_Scripts/openmpi_node/2.1.0 "))
# Print the RSpec to the enclosing page.
portal.context.printRequestRSpec(request)