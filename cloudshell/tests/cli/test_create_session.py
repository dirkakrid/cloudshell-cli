import unittest
from cloudshell.cli.cli import CLI
from cloudshell.cli.session.ssh_session import SSHConnectionParams
from cloudshell.cli.session.tcp_session import TCPConnectionParams
from cloudshell.cli.session_pool_manager import SessionPoolManager
from cloudshell.cli.command_mode import CommandMode

class CreateSessionTestCases(unittest.TestCase):

    def test_create_session(self):

        pool = SessionPoolManager(max_pool_size=1)
        cli = CLI(session_pool=pool)
        mode = CommandMode(r'%\s*$')

        connection_params = SSHConnectionParams(host='192.168.28.150',username='root',password='Juniper')
        connection_params2 = TCPConnectionParams(host='192.168.28.150', port=2483)

        auto_connections_list = [connection_params,connection_params2]

        with cli.get_session(auto_connections_list, mode) as default_session:
            out = default_session.send_command('show version', error_map={'srx220h-poe': 'big error'})
            print(out)
            # config_command_mode = ConfigCommandMode(context)
            # config_command_mode.add_parent_mode(mode)
            # with default_session.enter_mode(config_command_mode) as config_session:
            #     out = config_session.send_command('show interfaces')
            #     print(out)
            #     out = config_session.send_command('show interfaces', logger=cli.logger)
            #     print(out)

if __name__ == '__main__':
    unittest.main()
