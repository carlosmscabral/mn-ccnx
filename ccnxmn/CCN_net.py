
#import os
#import re
#import select
#import signal
#from time import sleep
#from itertools import chain

#from mininet.cli import CLI
#from mininet.log import info, error, debug, output
#from mininet.node import Host, OVSKernelSwitch, Controller
#from mininet.link import Link, Intf
#from mininet.util import quietRun, fixLimits, numCores, ensureRoot
#from mininet.util import macColonHex, ipStr, ipParse, netParse, ipAdd
#from mininet.term import cleanUpScreens, makeTerms

from mininet.log import info
from mininet.link import Link, Intf
from mininet.node import Host, OVSKernelSwitch, Controller
from mininet.util import ipStr, ipParse
from mininet.net import Mininet


def nextCCNnet(curCCNnet):
    netNum = ipParse(curCCNnet)
    return ipStr(netNum+4)


class CCNxMininet(Mininet):
    def __init__( self, topo=None, switch=OVSKernelSwitch, host=Host,
                  controller=Controller, link=Link, intf=Intf,
                  build=True, xterms=False, cleanup=False, ipBase='10.0.0.0/8',
                  inNamespace=False,
                  autoSetMacs=False, autoStaticArp=False, autoPinCpus=False,
                  listenPort=None ):

        self.ccnNetBase = '1.0.0.0'

        Mininet.__init__( self, topo, switch, host, controller, link, intf,
                          build, xterms, cleanup, ipBase, inNamespace,
                          autoSetMacs, autoStaticArp, autoPinCpus, listenPort )

    def isCCNhost(self, node):
        if 'fib' in node.params:
            return True
        else:
            return False

    def configHosts( self ):
        "Configure a set of hosts."
        for host in self.hosts:
            info( host.name + ' ' )
            intf = host.defaultIntf()
            if self.isCCNhost(host):
                host.configCCN()
                host.configDefault(ip=None,mac=None)
            elif intf:
                host.configDefault()
            else:
                # Don't configure nonexistent intf
                host.configDefault( ip=None, mac=None )
            # You're low priority, dude!
            # BL: do we want to do this here or not?
            # May not make sense if we have CPU lmiting...
            # quietRun( 'renice +18 -p ' + repr( host.pid ) )
            # This may not be the right place to do this, but
            # it needs to be done somewhere.
            host.cmd( 'ifconfig lo up' )
        info( '\n' )

    def buildFromTopo( self, topo=None ):
        """Build mininet from a topology object
           At the end of this function, everything should be connected
           and up."""

        # Possibly we should clean up here and/or validate
        # the topo
        if self.cleanup:
            pass

        info( '*** Creating network\n' )

        if not self.controllers and self.controller:
            # Add a default controller
            info( '*** Adding controller\n' )
            classes = self.controller
            if type( classes ) is not list:
                classes = [ classes ]
            for i, cls in enumerate( classes ):
                self.addController( 'c%d' % i, cls )

        info( '*** Adding hosts:\n' )
        for hostName in topo.hosts():
            self.addHost( hostName, **topo.nodeInfo( hostName ) )
            info( hostName + ' ' )

        info( '\n*** Adding switches:\n' )
        for switchName in topo.switches():
            self.addSwitch( switchName, **topo.nodeInfo( switchName) )
            info( switchName + ' ' )

        info( '\n*** Adding links:\n' )
        for srcName, dstName in topo.links(sort=True):
            src, dst = self.nameToNode[ srcName ], self.nameToNode[ dstName ]
            params = topo.linkInfo( srcName, dstName )
            srcPort, dstPort = topo.port( srcName, dstName )
            self.addLink( src, dst, srcPort, dstPort, **params )

            if self.isCCNhost(src):
                src.setIP(ipStr(ipParse(self.ccnNetBase) + 1) + '/30', intf=src.name + '-eth' + str(srcPort))
                dst.setIP(ipStr(ipParse(self.ccnNetBase) + 2) + '/30', intf=dst.name + '-eth' + str(dstPort))
                self.ccnNetBase=nextCCNnet(self.ccnNetBase)

            info( '(%s, %s) ' % ( src.name, dst.name ) )

        info( '\n' )

