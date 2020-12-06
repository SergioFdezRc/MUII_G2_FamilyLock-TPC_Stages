from mininet.net import Mininet
from mininet.node import Controller, RemoteController, Node
from mininet.cli import CLI
from mininet.log import setLogLevel, info
from mininet.link import Link, Intf

import sys
import numpy

def createTraffic(matrix, hosts):
	for s in range(0, len(hosts)):
		hosts[s].cmdPrint("iperf -s -u -i 1 -y C >> iperfServers.csv &")
		for c in range(0, len(hosts)):
			if hosts[s] != hosts[c]:
				hosts[c].cmpPrint("iperf -c "+s.IP()+" -u -b "+matrix[s][c]+" -t 10 -i 1 -y C >> iperfClients.csv &")

def createGenericTopo(self, remote_controller, controller_ip, controller_port, houses = 1, max_houses = 0):
	
	net = Mininet(topo = None, build = False)
	
	net.addController('controller', controller = remote_controller, ip = controller_ip, port = controller_port)

	hosts, switches, general_switches = [], [], []

	for house in range(houses):
		s = net.addSwitch('s' + (len(switches) + 1))
		switches.append(s)

		for host in range(1, 5):
			h = net.addHost('h' + (len(hosts) + 1))
			hosts.append(h)
		
			# Add Link
			net.addLink(h,s)

		if (house < (max_houses * (len(general_switches) + 1))):
			gs = net.addSwitch('gs' + (len(general_switches) + 1))
			general_switches.append(gs)
			net.addLink(s, gs)

	for i in range(len(general_switches) - 1):
		net.addLink(general_switches[i], general_switches[i + 1])

	matrix = numpy.ones((len(hosts), len(hosts)))
	numpy.fill_diagonal(matrix, 0)

	net.start()

	CLI(net)
	createTraffic(matrix, hosts)
	
	net.stop()

'''		
if __name__=='__main__':
	setLogLevel( 'info' )
	if (len(sys.argv) > 0):
		if (sys.argv[0] > 1 and sys.argv[1] > 0):
			createNet(sys.argv[0], sys.argv[1])
		else:
			print("There has to be more than 1 house and at least, 1 general switch.")
	else:
		createNet()
'''