from pox.core import core
import pox.openflow.libopenflow_01 as of
from pox.lib.revent import *
from pox.lib.util import dpidToStr
from pox.lib.addresses import EthAddr
from collections import namedtuple
import os
import csv
''' Add your imports here ... '''



log = core.getLogger()
policyFile = "%s/pox/pox/misc/firewall-policies.csv" % os.environ[ 'HOME' ]
pairs = []
with open(policyFile) as csvfile:
    readCSV = csv.reader(csvfile, delimiter=',')
    for row in readCSV:
        # row[0] = id (not needed?), row[1] = mac_0, row[2] = mac[1]
        pairs.append([row[1],row[2]])
    # remove first row of labels
    print(pairs)
    pairs.pop(0)

''' Add global variables and data processing here ... '''



class Firewall (EventMixin):

    def __init__ (self):
        self.listenTo(core.openflow)
        log.debug("Enabling Firewall Module")

    def _handle_ConnectionUp (self, event):
        ''' Add your logic here ... '''
        for pair in pairs:
                # will this work both ways???
                # define a new match condition between the two MAC addresses
                match = of.ofp_match()
                match.dl_src = EthAddr(pair[0])
                match.dl_dst = EthAddr(pair[1])
                # create a new flow table modification message
                msg = of.ofp_flow_mod()
                # execute this flow table's action for connections that match
                msg.match = match
                # send the flow table entry to the switch
                event.connection.send(msg)
                # by not attaching any action to this message, a packet that
                # matches the condition will be dropped

        log.debug("Firewall rules installed on %s", dpidToStr(event.dpid))

def launch ():
    '''
    Starting the Firewall module
    '''
    core.registerNew(Firewall)
