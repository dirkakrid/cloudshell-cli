from collections import OrderedDict
from cloudshell.cli.session.connection_manager import ConnectionManager
sessions_map = {'ssh':'SSHSession','telnet':'TelnetSession','tcp':'TCPSession','auto':'auto'}
def _get_session_type(argument):
    session_types = {
        'ssh': __import__('cloudshell.cli.session.ssh_session', fromlist=[sessions_map['ssh']]),
        'telnet': __import__('cloudshell.cli.session.tcp_session', fromlist=[sessions_map['telnet']]),
        'tcp': __import__('cloudshell.cli.session.telnet_session', fromlist=[sessions_map['tcp']])
    }
    func = session_types.get(argument, lambda: "auto")
    if (argument in sessions_map):
        return getattr(func, sessions_map.get(argument))
    else:
        return None

def _initiate_connection_manager(logger,session_type,session,default_prompt,session_pool_size,pool_timeout):
    CONNECTION_MAP=OrderedDict()
    CONNECTION_MAP[session_type] = session
    return ConnectionManager(logger,CONNECTION_MAP,session_type,default_prompt,session_pool_size,pool_timeout,config=None)
