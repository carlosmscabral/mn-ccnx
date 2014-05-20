from mininet.node import Node, Host, CPULimitedHost

class CCNHost( Host ):
  "CCNHost is a Host that always runs the ccnd daemon"

  def __init__( self, name, **kwargs ):
    Host.__init__( self, name, **kwargs )

    if not CCNHost.inited:
        CCNHost.init()

    self.cmd("export CCND_DEBUG=6")
    self.cmd("export CCND_LOG=./log.{0}".format(self.name))
#   print self.params['cache']

    if self.params['cache'] != None:
      self.cmd("export CCND_CAP={0}".format(self.params['cache']))

    self.cmd("export CCN_LOCAL_SOCKNAME=/tmp/.sock.ccnx.{0}".format(self.name))
    self.cmd("ccndstart")
    self.peerList = {}

    def config( self, fib=None, app=None, cache=None, **params ):
      r = Node.config( self, **params )

      self.setParam( r, 'app', fib=fib )
      self.setParam( r, 'fib', app=app)
      self.setParam( r, 'cache', cache=cache )

      return r

    def configCCN(self):
      self.buildPeerIP()
      self.setFIB()

    def buildPeerIP(self):
      for iface in self.intfList():
        link = iface.link
        
        if link:
          node1, node2 = link.intf1.node, link.intf2.node
          
          if node1 == self:
            self.peerList[node2.name] = link.intf2.node.IP(link.intf2)
            
          else:
            self.peerList[node1.name] = link.intf1.node.IP(link.intf1)


    def setFIB(self):
      for name in self.params['fib']:
        if not name:
          pass
          
        else:
          self.insert_fib(name[0],self.peerList[name[1]])


    def insert_fib(self, uri, host):
      self.cmd('ccndc add {0} tcp {1}'.format(uri,host))
 #    self.cmd('ccndc add {0} udp {1}'.format(uri,host))

    def terminate( self ):
      "Stop node."
      self.cmd('ccndstop')
      self.cmd('killall -r zebra ospf')
      Host.terminate(self)

    inited = False

    @classmethod
    def init( cls ):
      "Initialization for CCNHost class"
      cls.inited = True

class CPULimitedCCNHost( CPULimitedHost ):
  '''CPULimitedCCNHost is a Host that always runs the ccnd daemon and extends CPULimitedHost.
     It should be used when one wants to limit the resources of CCN routers and hosts '''


  def __init__( self, name, sched='cfs', **kwargs ):
    CPULimitedHost.__init__( self, name, sched, **kwargs )

    if not CCNHost.inited:
      CCNHost.init()

    self.cmd("export CCND_DEBUG=6")
    self.cmd("export CCND_LOG=./log.{0}".format(self.name))

    if self.params['cache'] != None:
      self.cmd("export CCND_CAP={0}".format(self.params['cache']))

    self.cmd("export CCN_LOCAL_SOCKNAME=/tmp/.sock.ccnx.{0}".format(self.name))
    self.cmd("ccndstart")
    self.peerList = {}

  def config( self, fib=None, app=None, cpu=None, cores=None, cache=None, **params):
    r = CPULimitedHost.config(self,cpu,cores, **params)

    self.setParam( r, 'app', fib=fib )
    self.setParam( r, 'fib', app=app)
    self.setParam( r, 'cache', cache=cache)

    return r

  def configCCN(self):
    self.buildPeerIP()
    self.setFIB()


  def buildPeerIP(self):
    for iface in self.intfList():
      link = iface.link
      
      if link:
        node1, node2 = link.intf1.node, link.intf2.node
        
        if node1 == self:
          self.peerList[node2.name] = link.intf2.node.IP(link.intf2)
          
        else:
          self.peerList[node1.name] = link.intf1.node.IP(link.intf1)


  def setFIB(self):
    for name in self.params['fib']:
      if not name:
        pass
        
      else:
        self.insert_fib(name[0],self.peerList[name[1]])


  def insert_fib(self, uri, host):
    self.cmd('ccndc add {0} tcp {1}'.format(uri,host))
#   self.cmd('ccndc add {0} udp {1}'.format(uri,host))

  def terminate( self ):
    "Stop node."
    self.cmd('ccndstop')
    self.cmd('killall -r zebra ospf')
    Host.terminate(self)

  inited = False


  @classmethod
  def init( cls ):
    "Initialization for CCNHost class"
    cls.inited = True

