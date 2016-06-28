from mininet.topo import Topo
from mininet.net import Mininet
from mininet.link import TCLink
from mininet.util import custom

# Topology to be instantiated in Mininet
class ComplexTopo(Topo):
    "Mininet Complex Topology"

    def __init__(self, cpu=.1, max_queue_size=None, **params):

        # Initialize topo
        Topo.__init__(self, **params)

        #Ethernet: Bandwidth 20 Mbps, Delay 1 ms, and loss rate 0% 
		#WiFi: Bandwidth 10 Mbps, Delay 3 ms, and loss rate 3% 
		#3G: Bandwidth 2 Mbps, Delay 10 ms, and loss rate 10%	

        #TODO: Create your Mininet Topology here!
		# h and link configuration
        hostConfig = {'cpu': cpu}
        
        linkConfigeth = {'bw': 20, 'delay': '1ms', 'loss': 0,
                   'max_queue_size': max_queue_size }
        linkConfigwifi = {'bw': 10, 'delay': '3ms', 'loss': 3 ,
                   'max_queue_size': max_queue_size }
        linkConfig3g = {'bw': 2, 'delay': '10ms', 'loss': 10,
                   'max_queue_size': max_queue_size }

        # hosts and switches
        s1 = self.addSwitch('s1')
        s2 = self.addSwitch('s2')
        s3 = self.addSwitch('s3')
        s4 = self.addSwitch('s4')

        h1= self.addHost('h1', **hostConfig)
        h2 = self.addHost('h2', **hostConfig)
        h3 = self.addHost('h3', **hostConfig)

        # Wire h1 to h2
        self.addLink(h1, s1, **linkConfigeth)
        self.addLink(s1,s2, **linkConfigeth)
        self.addLink(s2, s3, **linkConfigeth)
        self.addLink(s3, h2, **linkConfigwifi)

        # Wire h3 to rest
        self.addLink(s2, s4, **linkConfigeth)
        self.addLink(s4, h3, **linkConfig3g)
