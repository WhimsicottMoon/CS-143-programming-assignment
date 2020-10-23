from mininet.topo import Topo

class CustomTopo(Topo):
    "Simple Data Center Topology"

    "linkopts# - (1: core, 2: aggregation, 3: edge) link parameters"
    "fanout - number of child switches per parent switch"
    def __init__(self, linkopts1, linkopts2, linkopts3, fanout=2, **opts):
        ''' Initialize topology and default options '''
        Topo.__init__(self, **opts)
        
        ''' Add your logic here ... '''

        
                    
topos = { 'custom': ( lambda: CustomTopo() ) }

# Uncomment below (or write your own code) to test your topology
#linkopts1 = dict(bw=10, delay="5ms", loss=10, max_queue_size=1000, use_htb=True)
#linkopts2 = dict(bw=10, delay="5ms", loss=10, max_queue_size=1000, use_htb=True)
#linkopts3 = dict(bw=10, delay="5ms", loss=10, max_queue_size=1000, use_htb=True)
#topos = { "custom": ( lambda: CustomTopo(linkopts1,linkopts2,linkopts3) ) }