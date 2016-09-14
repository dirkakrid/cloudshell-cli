from cloudshell.cli.prompt_mode import Mode
from cloudshell.cli.service.cli_service import CliService
import cloudshell.cli.session_handler as session_handler


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
        #return self.session

    def set_default_actions(self,default_actions_tuple):pass

    def initial_commands(self,actions):
        '''
        :param actions: [(action1,prompt),(action2,prompt)...] or (action,prompt)
        :return: None
        '''
        self._set_actions(actions)

    def run_command(self,command,command_input=dict()):
        print self.session.hardware_expect('show version')

    def set_default_mode(self,mode_tuple):
        self.default_mode(mode_tuple)

    def set_modes(self,modes_tuple):
        self.set_different_modes(modes_tuple)

    def set_exit_mode_command(self,exit_command_tuple):
        self.exit_mode(exit_command_tuple)

c=Cli()

#print c.new_session(session_type='ssh',ip='192.168.42.235',user='root',password='Password1')
#print c.session.run_command('')

from cloudshell.cli.cli import Cli

cli = Cli()
cli.set_default_actions([('action1','prompt'),('action2','prompt')])
cli.set_default_mode(('default','prompt'))
cli.set_modes([('state2','prompt')])
cli.set_exit_mode_command(('exit','prompt'))

with cli.new_session(session_type='ssh',ip='192.168.42.235',user='root',password='Password1') as default_session:
    default_session.run_command('show version')

'''



TODO: with default_session.enter_mode('state2',enter_command='config t', exit_command='exit') as admin


from cloudshell.cli.cli import Cli

cli = Cli()

cli.set_default_actions([('action1','prompt'),('action2','prompt')] or ('action','prompt'))
cli.set_default_mode('default','prompt')
cli.set_modes([('state2','prompt')] or ('state','prompt'))
cli.set_exit_mode_command(('exit','prompt'))

with cli.new_session(session_type='ssh',ip='192.168.42.235',user='root',password='Password1') as default_session:
    with default_session.enter_mode('state2',command='config t') as admin:
        admin.run_command('show version',expected_map={'are you sure':'yes'},expected_str='prompt')
        admin.run_command('blbla', expected_map={'are you sure': 'yes'}, expected_str='prompt')
        with admin.enter_mode('state3',command='config b') as admin2:
            admin2.run_command('blabla', expected_map={'are you sure': 'yes'}, expected_str='prompt')
        default_session.run_command('bla bla')
'''


























