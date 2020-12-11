from mininet.net import Mininet
from mininet.node import Controller, RemoteController, Node
from mininet.cli import CLI
from mininet.log import setLogLevel, info
from mininet.link import Link, Intf

import sys
import numpy

def createTraffic(hosts, server):
	server.cmdPrint("iperf -s -u -i 1 -y C &")
	for c in range(0, len(hosts)):
		server.cmdPrint("iperf -c "+hosts[c].IP()+" -u -b 1 -t 10 -i 1 -y C >> iperfServer.csv &")
		hosts[c].cmdPrint("iperf -c "+server.IP()+" -u -b 1 -t 10 -i 1 -y C >> iperf.csv &")

def createGenericTopo(houses = 1):
	
	net = Mininet(topo = None, build = False)
	
	net.addController('controller', controller = RemoteController, ip = '127.0.0.1', port = 6633)

	hosts, switches = [], []
	
	gs = net.addSwitch('gs0')
	
	server = net.addHost('server0')
	net.addLink(server,gs)

	for house in range(houses):
		s = net.addSwitch('s' + str((len(switches) + 1)))
		switches.append(s)
		net.addLink(s,gs)

		for host in range(1, 5):
			h = net.addHost('h' + str((len(hosts) + 1)))
			hosts.append(h)
		
			# Add Link
			net.addLink(h,s)

	#matrix = numpy.ones((len(hosts), len(hosts)))
	#numpy.fill_diagonal(matrix, 0)

	net.start()

	CLI(net)
	createTraffic(hosts, server)
	
	net.stop()
		
if __name__=='__main__':
	setLogLevel( 'info' )
	if (len(sys.argv) > 1):
		createGenericTopo(int(sys.argv[1]))		
	else:
		print("No parameters specified, using just one house.")
		createGenericTopo()

