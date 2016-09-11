from cloudshell.cli.session.session_creator import SessionCreator



class Cli(object):

    def __init__(self,user,password,ip,port,mode='default'):
        self.sessions_map = {'ssh':'SSHSession','telnet':'TelnetSession','tcp':'TCPSession'}

    def __enter__(self):
        pass


    def __exit__(self, type, value, traceback):
        pass


    def ssh_session(self):
        pass

    def get_session_type(self,argument):
        switcher = {

            'ssh': __import__('cloudshell.cli.session.ssh_session', fromlist=[self.sessions_map['ssh']]),
            'telnet': __import__('cloudshell.cli.session.ssh_session',fromlist=[self.sessions_map['telnet']]),
            'tcp':__import__('cloudshell.cli.session.ssh_session',fromlist=[self.sessions_map['tcp']]),
        }
        # Get the function from switcher dictionary
        func = switcher.get(argument, lambda: "nothing")
        # Execute the function
        if(argument in self.sessions_map):
            return getattr(func, self.sessions_map.get(argument))
        else:
            return None


c=Cli('admin','admin','111',80)

print c.get_session_type('ssh')