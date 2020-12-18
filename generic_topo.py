from mininet.net import Mininet
from mininet.node import Controller, RemoteController, Node
from mininet.cli import CLI
from mininet.log import setLogLevel, info
from mininet.link import Link, Intf
import time

import sys

def createTest(hosts, server, bandwidth, test_name, folder_name):
	server_filename = folder_name + "iperfServer" + test_name + ".csv"
	client_filename = folder_name + "iperfClient" + test_name + ".csv"
	
	# Ping to discovery the topology
	for client in hosts:
		client.cmdPrint("ping -c3 " + server.IP())
	
	# From server to client
	server.cmdPrint("iperf -u -s -y C >> " + server_filename + " &")

	for client in hosts:
		# From client to server
		client.cmdPrint("iperf -u -c "+ server.IP()+" -b " + bandwidth + " -t 10 -i 1 -y C >> " + client_filename + " &")
		# Wait (0.1 * num_host) sec
		time.sleep(len(hosts)*4/100)

def createTraffic(test, houses, hosts, server):

	folder_name = ""

	if houses == 1:
		folder_name = "stage-small/"
	elif houses == 50:
		folder_name = "stage-medium/"
	elif houses == 250:
		folder_name = "stage-big/" 
	
	if test == 1:
		# Test 1 (Bandwith 10 MB/s, Time 10 sec, Interval 1 sec)
		print("Creating test 1")
		createTest(hosts, server, "10m", "Test1", folder_name)
		
	elif test == 2:
		# Test 2 (Bandwith 100 MB/s, Time 10 sec, Interval 1 sec)
		print("Creating test 2")
		createTest(hosts, server, "100m", "Test2",folder_name)

	elif test == 3:
		# Test 3 (Bandwith 1000 MB/s, Time 10 sec, Interval 1 sec)
		print("Creating test 3")
		createTest(hosts, server, "1000m", "Test3", folder_name)
	

def createGenericTopo(houses = 1, test = 1):
	
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

	print("Starting simulation")
	net.start()

	print("Waiting for connection")
	net.waitConnected()

	print("Creating traffic")
	createTraffic(test, houses, hosts, server)

	CLI(net)
	
	net.stop()
		
if __name__=='__main__':
	setLogLevel( 'info' )
	if (len(sys.argv) > 1):
		createGenericTopo(int(sys.argv[1]), int(sys.argv[2]))		
	else:
		print("No parameters specified, using just one house.")
		createGenericTopo()

