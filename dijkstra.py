from pox.core import core
import pox.openflow.libopenflow_01 as of
from pox.lib.revent import *
from pox.lib.util import dpidToStr
from pox.lib.addresses import EthAddr
from collections import namedtuple
import os
import csv

log = core.getLogger()
delayFile = "%s/pox/pox/misc/delay.csv" % os.environ[ 'HOME' ]
with open(delayFile, mode='r') as infile:
    reader = csv.reader(infile)
    delay_dict = {rows[0]:rows[1] for rows in reader}
    delay_dict.pop("link")

def dijkstra(s,d):
    source = s
    delay = {}
    adj_node = {}
    queue = []
    graph = {
            
        'S11': {'S12':delay_dict["g"], 'S18':delay_dict["k"]},
        'S12': {'S11':delay_dict["g"], 'S14':delay_dict["h"], 'S16':delay_dict["m"], 'S18':delay_dict["l"]},
        'S14': {'S12':delay_dict["h"], 'S16':delay_dict["i"], 'S18':delay_dict["n"]},
        'S16': {'S12':delay_dict["m"], 'S14':delay_dict["i"], 'S18':delay_dict["j"]},
        'S18': {'S11':delay_dict["k"], 'S12':delay_dict["l"], 'S14':delay_dict["n"], 'S16':delay_dict["j"]}
            
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

def dijkstra_wrapper(s,d):
    return dijkstra(s,d)[1]

class Dijkstra (EventMixin):

    def __init__ (self):
        self.listenTo(core.openflow)
        log.debug("Enabling Dijkstra Module")

    def _handle_ConnectionUp (self, event):    
        ''' Add your logic here ... '''
        
        log.debug("Dijkstra installed on %s", dpidToStr(event.dpid))        

def launch ():
    '''
    Starting the Dijkstra module
    '''
    core.registerNew(Dijkstra)
