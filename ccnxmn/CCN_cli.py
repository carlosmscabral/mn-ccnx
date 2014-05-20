from mininet.cli import CLI
from mininet.log import output

class CCNxCLI(CLI):
  prompt = 'miniccnx> '

  def do_ccndump(self, _line):
    "Dump FIB entries"
    for node in self.mn.values():
      if 'fib' in node.params:
        output(node.name + ': ')
        
        for name in node.params['fib']:
          output(str(name) + ' ')
          
        output('\n')
