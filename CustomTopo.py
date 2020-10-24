#!/usr/bin/python
from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import CPULimitedHost
from mininet.link import TCLink
from mininet.util import irange, dumpNodeConnections
from mininet.log import setLogLevel

'''
    "Simple Data Center Topology"

    "linkopts# - (1: core, 2: aggregation, 3: edge) link parameters"
    "fanout - number of child switches per parent switch"
'''
class CustomTopo(Topo):
    def __init__(self, linkopts1, linkopts2, linkopts3, fanout=2, **opts):
        #Initialize topology and default options
        Topo.__init__(self, **opts)
        
        self.fanout = fanout

        core = self.addSwitch("c1")
        aggregation_switches = []
        edge_switches = []
        hosts = []
        
        #core to aggregation
        for i in irange(1, fanout):
            name = "a" + str(i)
            aggregation_switches.append(self.addSwitch(name))
            self.addLink(core, aggregation_switches[i-1], **linkopts1)

        host = self.addHost("h1")

linkopts1 = dict(bw=10, delay="5ms", loss=10, max_queue_size=1000, use_htb=True)
linkopts2 = dict(bw=10, delay="5ms", loss=10, max_queue_size=1000, use_htb=True)
linkopts3 = dict(bw=10, delay="5ms", loss=10, max_queue_size=1000, use_htb=True)
topos = CustomTopo(linkopts1, linkopts2, linkopts3)
net = Mininet(topo=topos, host=CPULimitedHost, link=TCLink)
net.start()
net.stop()
