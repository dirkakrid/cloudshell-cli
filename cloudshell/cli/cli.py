from cloudshell.cli.session.session_creator import SessionCreator
from cloudshell.cli.session.session_proxy import ReturnToPoolProxy
from collections import OrderedDict
from cloudshell.cli.prompt_mode import Mode
from cloudshell.cli.service.cli_service import CliService
import cloudshell.cli.session_handler as session_handler
from types import ModuleType

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


    def __enter__(self):
        pass

    def __exit__(self, type, value, traceback):
        pass

    def new_session(self,session_type,ip,port='',user='',password='',input_map={},error_map={},session_pool_size=1,pool_timeout = 100):

        self.session = session_handler.initiate_connection_manager(self.logger,session_type,ip,port,user,password,self.default_prompt)


    def initial_commands(self,actions):
        '''
        :param actions: [(action1,prompt),(action2,prompt)...] or (action,prompt)
        :return: None
        '''
        self._set_actions(actions)

    def run_command(self,command,command_input=dict()):
        print self.session.hardware_expect('show version')

c=Cli()

print c.new_session(session_type='ssh',ip='192.168.42.235',user='root',password='Password1')
print c.session.run_command('')