from cloudshell.cli.prompt_mode import Mode
from cloudshell.cli.service.cli_service import CliService
import cloudshell.cli.session_handler as session_handler
from collections import OrderedDict
from cloudshell.cli.session.connection_manager import SessionManager, ConnectionManager
from cloudshell.cli.session.session_validation_proxy import SessionValidationProxy
from cloudshell.cli.session.session_creator import SessionCreator
from cloudshell.cli.session_handler import SessionHandler

_sessions_map = {'ssh':'SSHSession','telnet':'TelnetSession','tcp':'TCPSession','auto':'auto'}
from logging import Logger

class Cli(Mode):

    def __init__(self):

        self.session = None
        self.logger = Logger('logger')
        self.cli_service = CliService(None)
        self.initiate_connection_obj = True
        self.initiate_actions = None
        self._logger = None
        self.session_manager = None



    def _get_session_type(self,argument):
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

    def new_session(self,session_type,ip,port='',user='',password='',input_map={},error_map={},session_pool_size=1,pool_timeout = 100):

        session = self._initiate_connection_manager(self.logger,session_type,ip,port,user,password,self.get_default_prompt())
        self.session = SessionHandler(session)
        return self.session

    def set_default_actions(self,default_actions_tuple):pass

    def initial_commands(self,actions):
        '''
        :param actions: [(action1,prompt),(action2,prompt)...] or (action,prompt)
        :return: None
        '''
        self._set_actions(actions)



    def _initiate_connection_manager(self,logger,session_type,ip,port,user,password,default_prompt,session_pool_size=1,pool_timeout=120):
        session = self._get_session(session_type,ip,port,user,password)
        CONNECTION_MAP=OrderedDict()
        CONNECTION_MAP[session_type] = session
        connection_manager = ConnectionManager.get_instance()
        connection_manager.logger = logger
        connection_manager.session_manager = SessionManager(logger=logger,connection_type=session_type,prompt=default_prompt,connection_map=CONNECTION_MAP)
        return connection_manager

    def _get_session(self,session_type,ip,port,user,password):
        session_class = self._get_session_type(session_type)
        session = SessionCreator(session_class)
        session.proxy = SessionValidationProxy
        session.kwargs = {'host': ip,
                               'port': port}
        if (user != '' and password != ''):
            session.kwargs.update({'username': user,
                                        'password': password})
        return session

    def set_states(self,states_tuple):
        self.set_different_modes(states_tuple)
        return self.state


c=Cli()



from cloudshell.cli.cli import Cli

cli = Cli()
cli.set_default_actions([('action1','prompt'),('action2','prompt')])
state = cli.set_states([('default','r.*[>$#]\s*$'),('admin','#\s*$')])

with cli.new_session(session_type='ssh',ip='192.168.42.235',user='root',password='Password1') as default_session:
    default_session.run_command('show version')
    with default_session.enter_mode(state.admin, enter_command='config t', exit_command='exit') as admin:
        print "ok"

'''

from cloudshell.cli.cli import Cli

cli = Cli()

cli.set_default_actions([('action1','prompt'),('action2','prompt')] or ('action','prompt'))
state = cli.set_states([('default','r'.*[>$#]\s*$'),('admin','#\s*$')]
#for example state.default will return the prompt of mode default

with cli.new_session(session_type='ssh',ip='192.168.42.235',user='root',password='Password1') as default_session:
    with default_session.enter_mode(state.admin,enter_command='config t', exit_command='exit') as admin
        admin.run_command('show version',expected_map={'are you sure':'yes'},expected_str='prompt')
        admin.run_command('blbla', expected_map={'are you sure': 'yes'}, expected_str='prompt')
        with admin.enter_mode(state.admin,command='config b') as admin2:
            admin2.run_command('blabla', expected_map={'are you sure': 'yes'}, expected_str='prompt')
        default_session.run_command('bla bla')


'''


























