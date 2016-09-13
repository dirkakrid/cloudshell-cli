from collections import OrderedDict
from cloudshell.cli.session.connection_manager import SessionManager, ConnectionManager
from cloudshell.cli.session.session_validation_proxy import SessionValidationProxy
from cloudshell.cli.session.session_creator import SessionCreator
from types import ModuleType

_sessions_map = {'ssh':'SSHSession','telnet':'TelnetSession','tcp':'TCPSession','auto':'auto'}

def _get_session_type(argument):
    session_types = {
        'ssh': __import__('cloudshell.cli.session.ssh_session', fromlist=[_sessions_map['ssh']]),
        'telnet': __import__('cloudshell.cli.session.tcp_session', fromlist=[_sessions_map['telnet']]),
        'tcp': __import__('cloudshell.cli.session.telnet_session', fromlist=[_sessions_map['tcp']])
    }
    func = session_types.get(argument, lambda: "auto")
    if (argument in _sessions_map):
        return getattr(func, _sessions_map.get(argument))
    else:
        return None

def _get_session(session_type,ip,port,user,password):
    session_class = _get_session_type(session_type)
    session = SessionCreator(session_class)
    session.proxy = SessionValidationProxy
    session.kwargs = {'host': ip,
                           'port': port}
    if (user != '' and password != ''):
        session.kwargs.update({'username': user,
                                    'password': password})
    return session

def initiate_connection_manager(logger,session_type,ip,port,user,password,default_prompt,session_pool_size=1,pool_timeout=120):
    session = _get_session(session_type,ip,port,user,password)
    CONNECTION_MAP=OrderedDict()
    CONNECTION_MAP[session_type] = session
    connection_manager = ConnectionManager.get_instance()
    connection_manager.logger = logger
    print CONNECTION_MAP
    connection_manager.session_manager = SessionManager(connection_map=CONNECTION_MAP)

    session = connection_manager.get_session_instance(connection_type=session_type, prompt=default_prompt)
    session.logger = logger

    session.hardware_expect('')

    connection_manager.return_session_instance(session)

    return connection_manager

