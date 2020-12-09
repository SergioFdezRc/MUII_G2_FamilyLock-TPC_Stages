from mininet.net import Mininet
from mininet.node import Controller, RemoteController, Node
from mininet.cli import CLI
from mininet.log import setLogLevel, info
from mininet.link import Link, Intf

import sys
import numpy

# TODO this traffic creator doesnt work
def createTraffic(matrix, hosts):
	for s in range(0, len(hosts)):
		hosts[s].cmdPrint("iperf -s -u -i 1 -y C >> iperfServers.csv &")
		for c in range(0, len(hosts)):
			if hosts[s] != hosts[c]:
				hosts[c].cmdPrint("iperf -c "+s.IP()+" -u -b "+matrix[s][c]+" -t 10 -i 1 -y C >> iperfClients.csv &")

def createGenericTopo(houses = 1):
	
	net = Mininet(topo = None, build = False)
	
	net.addController('controller', controller = RemoteController, ip = '127.0.0.1', port = 6633)

	hosts, switches = [], []

	gs = net.addSwitch('gs0')

	for house in range(houses):
		s = net.addSwitch('s' + str((len(switches) + 1)))
		switches.append(s)

		net.addLink(s, gs)

		for host in range(1, 5):
			h = net.addHost('h' + str((len(hosts) + 1)))
			hosts.append(h)
		
			# Add Link
			net.addLink(h,s)

	server = net.addHost('server1')
	net.addLink(server, gs)

	matrix = numpy.ones((len(hosts), len(hosts)))
	numpy.fill_diagonal(matrix, 0)

	net.start()

	CLI(net)
	createTraffic(matrix, hosts)
	
	net.stop()



if __name__ == '__main__':
	setLogLevel('info')

	createGenericTopo(houses = 100)
	# ring_topo = mediumStage()
	# meter regla de flood en todos los switches
	# debemos añadir la regla de action normal para que utilice el protocolo IP, y no solo el ARP
	# topos = {'ring_topo': (lambda: ring_topo())}
