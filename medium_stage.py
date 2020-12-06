from mininet.net import Mininet
from mininet.node import Controller, RemoteController, Node
from mininet.log import setLogLevel, info
from mininet.cli import CLI

CONTROLLER_IP = '127.0.0.1'


class mediumStage(Mininet):

    def __init__(self):
        Mininet.__init__(self, topo=None, build=False)
        self.addController('c0', controller=RemoteController, ip=CONTROLLER_IP, port=6633)
        _h1 = self.addHost("h1", ip='10.0.0.1')
        _h4 = self.addHost("h4", ip='10.0.0.2')

        _s1 = self.addSwitch("s1")
        _s2 = self.addSwitch("s2")
        _s3 = self.addSwitch("s3")
        _s4 = self.addSwitch("s4")

        self.addLink(_h1, _s1)
        self.addLink(_h4, _s4)

        self.addLink(_s1, _s2)
        self.addLink(_s1, _s3)
        self.addLink(_s1, _s4)

        self.addLink(_s2, _s3)
        self.addLink(_s2, _s4)

        self.addLink(_s3, _s4)
        self.start()
        CLI(self)


if __name__ == '__main__':
    setLogLevel('info')
    ring_topo = mediumStage()
#     meter regla de flood en todos los switches
# debemos añadir la regla de action normal para que utilice el protocolo IP, y no solo el ARP
# topos = {'ring_topo': (lambda: ring_topo())}
