
from cloudshell.cli.service.cli_service import CliService
from cloudshell.cli.session.session import Session




class SessionHandler(object):
    def __init__(self,session):
        """

        :param session:
         :type session: Session
        """

        self.session = session
        self.cli_service = CliService()

    def enter_mode(self):
        pass

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        print '__exit__()'

    def run_command(self,command,  prompt,command_input=dict()):
        print self.session.hardware_expect(data_str='show version',session=self.session)


        '''
        session = connection_manager.get_session_instance()


        session.hardware_expect('')

        connection_manager.return_session_instance(session)
        '''


