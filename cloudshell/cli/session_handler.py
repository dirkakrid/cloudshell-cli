
from cloudshell.cli.service.cli_service import CliService




class SessionHandler(object):
    def __init__(self,session):

        self.session = session
        self.cli_service = CliService()



    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        print '__exit__()'

    def run_command(self, command, command_input=dict()):
        print self.cli_service.send_command('show version',session=self.session)


        '''
        session = connection_manager.get_session_instance()


        session.hardware_expect('')

        connection_manager.return_session_instance(session)
        '''


