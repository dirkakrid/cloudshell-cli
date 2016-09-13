from cloudshell.cli.session.session_creator import SessionCreator
from cloudshell.cli.session.session_proxy import ReturnToPoolProxy
from collections import OrderedDict
from cloudshell.cli.prompt_mode import Mode
from cloudshell.cli.service.cli_service import CliService
import cloudshell.cli.configuration.cloudshell_cli_configuration as config



class Cli(Mode):

    def __init__(self):
        self.sessions_map = {'ssh':'SSHSession','telnet':'TelnetSession','tcp':'TCPSession','auto':'auto'}
        self.session = None

        self.cli_service = CliService()
        self.initiate_connection_obj = True
        self.initiate_actions = None

    def __enter__(self):
        pass

    def __exit__(self, type, value, traceback):
        pass

    def new_session(self,session_type,ip,port,user='',password='',session_pool_size=1,pool_timeout = 100):
        session_class = config._get_session_type(session_type)
        self.session = SessionCreator(session_class)
        self.session.proxy = ReturnToPoolProxy
        self.session.kwargs = {'host': ip,
                        'port': port}
        if(user!='' and password!=''):
            self.session.kwargs.update({'username': user,
                              'password': password})
        if(session_class):
            if(self.initiate_connection_obj):
                self.initiate_connection_obj = False
                config._initiate_connection_manager(session_type,self.session,self.default_prompt,session_pool_size,pool_timeout)



    def initial_commands(self,actions):
        '''
        :param actions: [(action1,prompt),(action2,prompt)...] or (action,prompt)
        :return: None
        '''
        self._set_actions(actions)

    def run_command(self,command,command_input=dict()):pass

c=Cli()

print c.get_session_type('ssh')