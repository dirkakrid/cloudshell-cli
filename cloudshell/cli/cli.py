from cloudshell.cli.session.session_creator import SessionCreator
from cloudshell.cli.session.session_proxy import ReturnToPoolProxy


class Cli(object):

    def __init__(self):
        self.sessions_map = {'ssh':'SSHSession','telnet':'TelnetSession','tcp':'TCPSession'}

    def __enter__(self):
        pass


    def __exit__(self, type, value, traceback):
        pass


    def get_session_type(self,argument):
        session_types = {
            'ssh': __import__('cloudshell.cli.session.ssh_session', fromlist=[self.sessions_map['ssh']]),
            'telnet': __import__('cloudshell.cli.session.ssh_session',fromlist=[self.sessions_map['telnet']]),
            'tcp':__import__('cloudshell.cli.session.ssh_session',fromlist=[self.sessions_map['tcp']]),
        }
        func = session_types.get(argument, lambda: "nothing")
        if(argument in self.sessions_map):
            return getattr(func, self.sessions_map.get(argument))
        else:
            return None


    def new_session(self,session_type,ip,port,user='',password=''):
        session_class = self.get_session_type(session_type)
        session = SessionCreator(session_class)
        session.proxy = ReturnToPoolProxy
        session.kwargs = {'host': ip,
                        'port': port}
        if(user!='' and password!=''):
            session.kwargs.update({'username': user,
                              'password': password})


c=Cli()

print c.get_session_type('ssh')