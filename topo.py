#!/usr/bin/python
from mininet.topo import Topo
from mininet.net import Mininet
import csv
from mininet.log import setLogLevel
from mininet.node import CPULimitedHost
from mininet.link import TCLink
from mininet.util import irange, dumpNodeConnections
import os

delayFile = "%s/pox/pox/misc/delay.csv" % os.environ[ 'HOME' ]

with open(delayFile, mode='r') as infile:
    reader = csv.reader(infile)
    delay_dict = {rows[0]:rows[1] for rows in reader}
    delay_dict.pop("link")

#print(delay_dict)
    
class Q9Topo(Topo):
    def __init__(self, **opts):
        ''' Initialize topology and default options '''
        Topo.__init__(self, **opts)

        switches = []
        hosts = []
        
        for switch in ["s11","s12","s14","s16","s18"]:
            switches.append(self.addSwitch(switch))
        for host in ["h13","h15","h17","h19"]:
            hosts.append(self.addHost(host))
        
        self.addLink(switches[0], switches[1], delay=delay_dict["g"]+"ms")
        self.addLink(switches[0], switches[-1], delay=delay_dict["k"]+"ms")
        self.addLink(switches[1], switches[2], delay=delay_dict["h"]+"ms")
        self.addLink(switches[1], switches[3], delay=delay_dict["m"]+"ms")
        self.addLink(switches[1], switches[4], delay=delay_dict["l"]+"ms")
        self.addLink(switches[2], switches[3], delay=delay_dict["i"]+"ms")
        self.addLink(switches[2], switches[4], delay=delay_dict["n"]+"ms") 
        self.addLink(switches[3], switches[4], delay=delay_dict["j"]+"ms")
        
        for i in range(4):
            self.addLink(switches[i+1], hosts[i])
        
        
        
setLogLevel("info")                   
topos = Q9Topo()
net = Mininet(topo=topos, host=CPULimitedHost, link=TCLink)
net.start()
print ("Dumping host connections")
dumpNodeConnections(net.hosts)
print ("Testing network connectivity")
net.pingAll()
net.stop()
