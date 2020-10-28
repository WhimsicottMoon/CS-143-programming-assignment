from pox.core import core
import pox.openflow.libopenflow_01 as of
from pox.lib.revent import *
from pox.lib.util import dpidToStr
from pox.lib.addresses import EthAddr
from collections import namedtuple
from pox.lib.addresses import IPAddr
import os
import csv

log = core.getLogger()
delayFile = "%s/pox/pox/misc/delay.csv" % os.environ[ 'HOME' ]
with open(delayFile, mode='r') as infile:
    reader = csv.reader(infile)
    delay_dict = {rows[0]:rows[1] for rows in reader}
    delay_dict.pop("link")
    for key in delay_dict:
        delay_dict[key] = int(delay_dict[key])
    

hosts = ["h13", "h15", "h17", "h19"]
host_IPs = ["10.0.0.1", "10.0.0.2", "10.0.0.3", "10.0.0.4"]
host_MACs = ["00:00:00:00:00:01","00:00:00:00:00:02","00:00:00:00:00:03","00:00:00:00:00:04"]

ports = {
        
        's11': {'s12': 1, 's18': 2},
        's12': {'s11':1, 's14': 2, 's16': 3, 's18': 4, 'h13': 5},
        's14': {'s12': 1, 's16': 2, 's18': 3, 'h15': 4},
        's16': {'s12': 1, 's14': 2, 's18': 3, 'h17': 4},
        's18': {'s11': 1, 's12': 2, 's14': 3, 's16': 4, 'h19': 5}
            
            }

def dijkstra(s,d):
    source = s
    delay = {}
    adj_node = {}
    queue = []
    graph = {
        'h13': {'s12':0},
        'h15': {'s14':0},
        'h17': {'s16':0},
        'h19': {'s18':0},
        's11': {'s12':delay_dict["g"], 's18':delay_dict["k"]},
        's12': {'s11':delay_dict["g"], 's14':delay_dict["h"], 's16':delay_dict["m"], 's18':delay_dict["l"], 'h13':0},
        's14': {'s12':delay_dict["h"], 's16':delay_dict["i"], 's18':delay_dict["n"], 'h15':0},
        's16': {'s12':delay_dict["m"], 's14':delay_dict["i"], 's18':delay_dict["j"], 'h17':0},
        's18': {'s11':delay_dict["k"], 's12':delay_dict["l"], 's14':delay_dict["n"], 's16':delay_dict["j"], 'h19':0}
            
            }

    for node in graph:
        delay[node] = float("inf")
        adj_node[node] = None
        queue.append(node)
    
    delay[source] = 0

    while queue:
        # find min distance which wasn't marked as current
        key_min = queue[0]
        min_val = delay[key_min]
        for n in range(1, len(queue)):
            if delay[queue[n]] < min_val:
                key_min = queue[n]  
                min_val = delay[key_min]
        cur = key_min
        queue.remove(cur)
        
        for i in graph[cur]:
            alternate = graph[cur][i] + delay[cur]
            if delay[i] > alternate:
                delay[i] = alternate
                adj_node[i] = cur
                
    final_list = []        
    final_list.append(d)
    while True:
        d = adj_node[d]
        if d is None:
            break
        final_list.append(d)
    final_list.reverse()
    
    return final_list

def next_in_path(s,d):
    if (s == d):
        return d
    else:
        return dijkstra(s,d)[1]

class Dijkstra (EventMixin):

    def __init__ (self):
        self.listenTo(core.openflow)
        log.debug("Enabling Dijkstra Module")

    def _handle_ConnectionUp (self, event):    
        current_switch = "s%s" % event.dpid
        for i in range(0, 4):
            #naking rules based on MAC addresses
            match = of.ofp_match()
            match.dl_dst = EthAddr(host_MACs[i])
            next_step = next_in_path(current_switch, hosts[i])
            out_port = ports[current_switch][next_step]
            # create a new flow table modification message
            msg = of.ofp_flow_mod()
            # assign this flow table message's match condition to the one above
            msg.match = match
            # make the action for this msg
            msg.actions.append(of.ofp_action_output(port = out_port))
            # send the flow table entry to the switch
            event.connection.send(msg)
            #making rules for ARP packets based on IP addresses
            match = of.ofp_match()
            match.dl_type = 0x806
            match.nw_dst = IPAddr(host_IPs[i])            
            next_step = next_in_path(current_switch, hosts[i])
            out_port = ports[current_switch][next_step]
            # create a new flow table modification message
            msg = of.ofp_flow_mod()
            # assign this flow table message's match condition to the one above
            msg.match = match
            # make the action for this msg
            msg.actions.append(of.ofp_action_output(port = out_port))
            # send the flow table entry to the switch
            event.connection.send(msg)
        log.debug("Dijkstra installed on %s", dpidToStr(event.dpid))        

def launch ():
    '''
    Starting the Dijkstra module
    '''
    core.registerNew(Dijkstra)
