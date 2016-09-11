from cloudshell.cli.session.session_creator import SessionCreator
from cloudshell.cli.session.session_proxy import ReturnToPoolProxy
from collections import OrderedDict

class Cli(object):

    def __init__(self):
        self.sessions_map = {'ssh':'SSHSession','telnet':'TelnetSession','tcp':'TCPSession'}
        self.session = None
        self.CONNECTION_MAP = OrderedDict()

    def __enter__(self):
        pass


    def __exit__(self, type, value, traceback):
        pass


    def _get_session_type(self,argument):
        session_types = {
            'ssh': __import__('cloudshell.cli.session.ssh_session', fromlist=[self.sessions_map['ssh']]),
            'telnet': __import__('cloudshell.cli.session.ssh_session',fromlist=[self.sessions_map['telnet']]),
            'tcp':__import__('cloudshell.cli.session.ssh_session',fromlist=[self.sessions_map['tcp']]),
        }
        func = session_types.get(argument, lambda: "auto")
        if(argument in self.sessions_map):

            return getattr(func, self.sessions_map.get(argument))
        else:
            return None


    def new_session(self,session_type,ip,port,user='',password=''):
        session_class = self._get_session_type(session_type)
        self.session = SessionCreator(session_class)
        self.session.proxy = ReturnToPoolProxy
        self.session.kwargs = {'host': ip,
                        'port': port}
        if(user!='' and password!=''):
            self.session.kwargs.update({'username': user,
                              'password': password})
        if(session_class):
            self.CONNECTION_MAP[session_type] = self.session


c=Cli()

print c.get_session_type('ssh')