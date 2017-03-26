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
	if i == 1:
		node.addService(rspec.Execute(shell="/bin/sh",
								command="sudo apt-get install -y nfs-kernel-server"))
		node.addService(rspec.Execute(shell="/bin/sh",
								command="echo \"/home *(rw,sync,no_root_squash)\" | sudo tee -a /etc/exports >> /dev/null"))
		node.addService(rspec.Execute(shell="/bin/sh",
								command="sudo systemctl start nfs-kernel-server.service"))
	else:
		node.addService(rspec.Execute(shell="/bin/sh",
								command="sudo apt-get install -y nfs-common"))
		node.addService(rspec.Execute(shell="/bin/sh",
								command="echo \"192.168.1.2:/home /local/home nfs rsize=8192,wsize=8192,timeo=14,intr\" | sudo tee -a /etc/exports >> /dev/null"))
# Print the RSpec to the enclosing page.
portal.context.printRequestRSpec(request)