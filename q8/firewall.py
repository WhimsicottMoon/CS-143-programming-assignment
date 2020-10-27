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
# parse csv which details which MACs to block
with open(policyFile) as csvfile:
    readCSV = csv.reader(csvfile, delimiter=',')
    for row in readCSV:
        # row[0] = id (not needed), row[1] = mac_0, row[2] = mac_1
        # add the two MAC addresses in each row of CSV to 'pairs' list
        pairs.append([row[1],row[2]])
        pairs.append([row[2],row[1]])
    # remove first two rows which will just be labels
    pairs.pop(0)
    pairs.pop(0)
    # debug
    print(pairs)

    # 'pairs' is a list of ordered pairs containing the MAC addresses
    # of two devices whose traffic we want to block.

''' Add global variables and data processing here ... '''



class Firewall (EventMixin):

    def __init__ (self):
        self.listenTo(core.openflow)
        log.debug("Enabling Firewall Module")

    def _handle_ConnectionUp (self, event):
        ''' Add your logic here ... '''
        # adds a flow table rule for each pair of MAC addresses in the list 'pairs'
        # that will block traffic from the first MAC addr to the second MAC addr
        #
        # a flow table rule consists of a match condition and an action.
        # by leaving the action attribute of a flow table rule empty, we cause
        # a packet that satisfies the match condition to be dropped.
        for pair in pairs:
                # define a new match condition between the two MAC addresses
                match = of.ofp_match()
                match.dl_src = EthAddr(pair[0])
                match.dl_dst = EthAddr(pair[1])
                # create a new flow table modification message
                msg = of.ofp_flow_mod()
                # assign this flow table messages match condition to the one
                # we made above, and leave it's action attribute empty
                msg.match = match
                # send the flow table entry to the switch
                event.connection.send(msg)

        log.debug("Firewall rules installed on %s", dpidToStr(event.dpid))

def launch ():
    '''
    Starting the Firewall module
    '''
    core.registerNew(Firewall)
