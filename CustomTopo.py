#Alexander Chen, Daniel Cisneros, Fred Kelly, Veronica Tang
#10/23/20

from mininet.topo import Topo
from mininet.net import Mininet
from mininet.util import irange,dumpNodeConnections
from mininet.log import setLogLevel

class CustomTopo(Topo):
    "Simple Data Center Topology"

    "linkopts# - (1: core, 2: aggregation, 3: edge) link parameters"
    "fanout - number of child switches per parent switch"
    def __init__(self, linkopts1, linkopts2, linkopts3, fanout=2, **opts):
        ''' Initialize topology and default options '''
        Topo.__init__(self, **opts)
        
        ''' Add your logic here ... '''
        self.fanout = fanout

        core = self.addSwitch("core")
        aggregation_switches = []
        edge_switches = []
        hosts = []
        
        #core to aggregation
        for i in irange(1, fanout):
            name = "Aggregation" + str(i)
            aggregation_switches.append(self.addSwitch(name))
            self.addLink(core, aggregation_switches[i-1], linkopts1)
   
                    
topos = { 'custom': ( lambda: CustomTopo() ) }

# Uncomment below (or write your own code) to test your topology
linkopts1 = dict(bw=10, delay="5ms", loss=10, max_queue_size=1000, use_htb=True)
linkopts2 = dict(bw=10, delay="5ms", loss=10, max_queue_size=1000, use_htb=True)
linkopts3 = dict(bw=10, delay="5ms", loss=10, max_queue_size=1000, use_htb=True)
topos = { "custom": ( lambda: CustomTopo(linkopts1,linkopts2,linkopts3) ) }
