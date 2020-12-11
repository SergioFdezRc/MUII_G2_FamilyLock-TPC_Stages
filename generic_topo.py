from mininet.net import Mininet
from mininet.node import Controller, RemoteController, Node
from mininet.cli import CLI
from mininet.log import setLogLevel, info
from mininet.link import Link, Intf
import time

import sys

def createTest(hosts, server, bandwith, test_name):
	server_filename = "iperfServer" + test_name + ".csv"
	client_filename = "iperfClient" + test_name + ".csv"
	
	# From server to client
	server.cmdPrint("iperf -s -u -y C >> " + server_filename + " &")

	for client in hosts:
		# From client to server
		client.cmdPrint("iperf -c "+ server.IP()+" -u -t 10 -i 1 -y C >> " + client_filename + " &")

def createTraffic(hosts, server):
	#server.cmdPrint("iperf -s -u -y C &")
	# Test 1 (Bandwith 10 MB/s, Time 10 sec, Interval 0 sec)
	print("Creating test 1")
	createTest(hosts, server, "1m", "Test1")
	'''
	# Test 2 (Bandwith 100 MB/s, Time 10 sec, Interval 0 sec)
	print("Creating test 2")
	createTest(hosts, server, 100, "Test2")
	# Test 3 (Bandwith 1000 MB/s, Time 10 sec, Interval 0 sec)
	print("Creating test 3")
	createTest(hosts, server, 1000, "Test3")
	# Test 4 (Bandwith 10 MB/s, Time 10 sec, Interval 1 sec)
	print("Creating test 4")
	createTest(hosts, server, 10, 10, 1, "Test4")
	# Test 5 (Bandwith 100 MB/s, Time 10 sec, Interval 1 sec)
	print("Creating test 5")
	createTest(hosts, server, 100, 10, 1, "Test5")
	# Test 6 (Bandwith 1000 MB/s, Time 10 sec, Interval 1 sec)
	print("Creating test 6")
	createTest(hosts, server, 1000, 10, 1, "Test6")
	'''
	

def createGenericTopo(houses = 1):
	
	net = Mininet(topo = None, build = False, autoSetMacs = True)
	
	net.addController('controller', controller = RemoteController, ip = '127.0.0.1', port = 6633)

	hosts, switches = [], []
	
	gs = net.addSwitch('s0')
	
	server = net.addHost('h0')
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

	net.start()

	createTraffic(hosts, server)
	CLI(net)
	
	net.stop()
		
if __name__=='__main__':
	setLogLevel( 'info' )
	if (len(sys.argv) > 1):
		createGenericTopo(int(sys.argv[1]))		
	else:
		print("No parameters specified, using just one house.")
		createGenericTopo()

