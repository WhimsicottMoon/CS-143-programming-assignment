from mininet.topo import Topo
import csv

with open('delay.csv', mode='r') as infile:
    reader = csv.reader(infile)
    delay_dict = {rows[0]:rows[1] for rows in reader}
    delay_dict.pop("link")
    
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
        
        
        
                    
topos = { 'custom': ( lambda: Q9Topo() ) }
