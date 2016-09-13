from cloudshell.cli.session.session_creator import SessionCreator
from cloudshell.cli.session.session_proxy import ReturnToPoolProxy
from collections import OrderedDict
from cloudshell.cli.prompt_mode import Mode
from cloudshell.cli.service.cli_service import CliService
import cloudshell.cli.session_handler as session_handler
import inject


class Cli(Mode):

    def __init__(self):

        self.session = None

        self.cli_service = CliService(None)
        self.initiate_connection_obj = True
        self.initiate_actions = None
        self._logger = None
        self.connection_manager = None

    @property
    def logger(self):
        if self._logger is None:
            try:
                self._logger = inject.instance('logger')
            except:
                raise Exception('SDNRoutingResolution', 'Logger is none or empty')
        return self._logger

    def __enter__(self):
        pass

    def __exit__(self, type, value, traceback):
        pass

    def new_session(self,session_type,ip,port='',user='',password='',input_map={},error_map={},session_pool_size=1,pool_timeout = 100):
        session_class = session_handler._get_session_type(session_type)
        self.session = SessionCreator(session_class)
        self.session.proxy = ReturnToPoolProxy
        self.session.kwargs = {'host': ip,
                        'port': port}
        if(user!='' and password!=''):
            self.session.kwargs.update({'username': user,
                              'password': password})
        if(session_class):
            self.cli_service.set_session_data(1,self.default_prompt,self.config_mode_prompt)
            if(self.initiate_connection_obj):
                self.initiate_connection_obj = False
                self.connection_manager = session_handler._initiate_connection_manager(self._logger,session_type,self.session,self.default_prompt,session_pool_size,pool_timeout)
        mn = self.connection_manager.get_session()
        print mn


    def initial_commands(self,actions):
        '''
        :param actions: [(action1,prompt),(action2,prompt)...] or (action,prompt)
        :return: None
        '''
        self._set_actions(actions)

    def run_command(self,command,command_input=dict()):pass

c=Cli()

print c.new_session(session_type='ssh',ip='192.168.42.235',user='root',password='Password1')