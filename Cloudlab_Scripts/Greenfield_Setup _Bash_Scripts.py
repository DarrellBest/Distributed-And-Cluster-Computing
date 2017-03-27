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
					
pc.defineParameter("database", "Name of controller node",
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
		
	#node.disk_image = "urn:publicid:IDN+emulab.net+image+emulab-ops:CENTOS66-64-STD"
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
	#setup nfs and password free ssh
	#server
	if i == 1:
		node.addService(rspec.Execute(shell="/bin/sh",
								command="wget 'https://raw.githubusercontent.com/DarrellBest/Distributed-And-Cluster-Computing/master/Cloudlab_Scripts/setup_nfs_server.sh' "))
		node.addService(rspec.Execute(shell="/bin/sh",
								command="./setup_nfs_server.sh"))
	#client								
	else:
		node.addService(rspec.Execute(shell="/bin/sh",
								command="wget'https://raw.githubusercontent.com/DarrellBest/Distributed-And-Cluster-Computing/master/Cloudlab_Scripts/setup_nfs_clients.sh'"))
		node.addService(rspec.Execute(shell="/bin/sh",
								command="./setup_nfs_clients.sh"))
								
	if i == 0:
		#must be in root to install torque
		#node.addService(rspec.Execute(shell="/bin/sh",
		#						command="sudo su"))
		#apt-get install torque
		node.addService(rspec.Execute(shell="/bin/sh",
								command="sudo apt-get install -y torque-server torque-client torque-mom torque-pam"))
		#stop the default torque server
		node.addService(rspec.Execute(shell="/bin/sh",
								command="/etc/init.d/torque-mom stop"))
		node.addService(rspec.Execute(shell="/bin/sh",
								command="/etc/init.d/torque-scheduler stop"))
		node.addService(rspec.Execute(shell="/bin/sh",
								command="/etc/init.d/torque-server stop"))
		#create custom torque server
		node.addService(rspec.Execute(shell="/bin/sh",
								command="yes | pbs_server -t create"))
		#kill custom torque server
		node.addService(rspec.Execute(shell="/bin/sh",
								command="killall pbs_server"))		
		#configure torque server
		node.addService(rspec.Execute(shell="/bin/sh",
								command="echo 'controllerHost-lan' | sudo tee /etc/torque/server_name"))
		node.addService(rspec.Execute(shell="/bin/sh",
								command="echo 'controllerHost-lan' | sudo tee /var/spool/torque/server_priv/acl_svr/acl_hosts"))
		node.addService(rspec.Execute(shell="/bin/sh",
								command="echo 'geniuser@controllerHost-lan' | sudo tee /var/spool/torque/server_priv/acl_svr/operators"))
		node.addService(rspec.Execute(shell="/bin/sh",
								command="echo 'geniuser@controllerHost-lan' | sudo tee /var/spool/torque/server_priv/acl_svr/managers"))
		node.addService(rspec.Execute(shell="/bin/sh",
								command="echo 'root@controllerHost-lan' | sudo tee -a /var/spool/torque/server_priv/acl_svr/operators"))
		node.addService(rspec.Execute(shell="/bin/sh",
								command="echo 'root@controllerHost-lan' | sudo tee -a /var/spool/torque/server_priv/acl_svr/managers"))
		
		#add work nodes to server
		node.addService(rspec.Execute(shell="/bin/sh",
								command="echo 'node2 np=4' | sudo tee /var/spool/torque/server_priv/nodes"))		
		node.addService(rspec.Execute(shell="/bin/sh",
								command="echo 'node3 np=4' | sudo tee -a /var/spool/torque/server_priv/nodes"))
		node.addService(rspec.Execute(shell="/bin/sh",
								command="echo 'node4 np=4' | sudo tee -a /var/spool/torque/server_priv/nodes"))								
		#configure mom
		node.addService(rspec.Execute(shell="/bin/sh",
								command="echo 'geniuser@controllerHost-lan' | sudo tee /var/spool/torque/mom_priv/config"))
		node.addService(rspec.Execute(shell="/bin/sh",
								command="echo 'root@controllerHost-lan' | sudo tee -a /var/spool/torque/mom_priv/config"))
		#start torque
		node.addService(rspec.Execute(shell="/bin/sh",
								command="/etc/init.d/torque-mom start"))
		node.addService(rspec.Execute(shell="/bin/sh",
								command="/etc/init.d/torque-scheduler start"))
		node.addService(rspec.Execute(shell="/bin/sh",
								command="/etc/init.d/torque-server start"))	
		#set scheduling properties
		node.addService(rspec.Execute(shell="/bin/sh",
								command="qmgr -c 'set server scheduling = True'"))
		node.addService(rspec.Execute(shell="/bin/sh",
								command="qmgr -c 'set server keep_completed = 300'"))
		node.addService(rspec.Execute(shell="/bin/sh",
								command="qmgr -c 'set server mom_job_sync = True'"))
		#create default queue
		node.addService(rspec.Execute(shell="/bin/sh",
								command="qmgr -c 'create queue batch'"))
		node.addService(rspec.Execute(shell="/bin/sh",
								command="qmgr -c 'set queue batch queue_type = execution'"))
		node.addService(rspec.Execute(shell="/bin/sh",
								command="qmgr -c 'set queue batch started = true'"))
		node.addService(rspec.Execute(shell="/bin/sh",
								command="qmgr -c 'set queue batch enabled = true'"))
		node.addService(rspec.Execute(shell="/bin/sh",
								command="qmgr -c 'set queue batch resources_default.walltime = 0:01:00'"))
		node.addService(rspec.Execute(shell="/bin/sh",
								command="qmgr -c 'set queue batch resources_default.nodes = 1'"))
		node.addService(rspec.Execute(shell="/bin/sh",
								command="qmgr -c 'set server default_queue = batch'"))	
		#configure submission pool
		node.addService(rspec.Execute(shell="/bin/sh",
								command="qmgr -c 'set server submit_hosts = controllerHost-lan'"))
		node.addService(rspec.Execute(shell="/bin/sh",
								command="qmgr -c 'set server allow_node_submit = true'"))					
	elif i != 1:
		#apt-get install torque
		node.addService(rspec.Execute(shell="/bin/sh",
								command="sudo apt-get install -y torque-client torque-mom"))
		#stop torque-mom
		node.addService(rspec.Execute(shell="/bin/sh",
								command="/etc/init.d/torque-mom stop"))
		#point client to server
		node.addService(rspec.Execute(shell="/bin/sh",
								command="echo 'controllerHost-lan' | sudo tee /etc/torque/server_name"))
		#start torque-mom
		node.addService(rspec.Execute(shell="/bin/sh",
								command="/etc/init.d/torque-mom start"))

# Print the RSpec to the enclosing page.
portal.context.printRequestRSpec(request)