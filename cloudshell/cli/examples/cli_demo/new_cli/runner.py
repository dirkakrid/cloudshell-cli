from cloudshell.cli.cli import CLI
from cloudshell.cli.session_pool_manager import SessionPoolManager
from cloudshell.core.logger.qs_logger import get_qs_logger
from connect_to_switch.SwitchClihandler import SwitchCliHandler
from cloudshell.shell.core.context import ResourceCommandContext, ResourceContextDetails, ReservationContextDetails,ConnectivityContext
from cloudshell.cli.command_mode import CommandMode
from cloudshell.shell.core.context_utils import get_attribute_by_name
logger = get_qs_logger()

def create_context():
    context = ResourceCommandContext()
    context.resource = ResourceContextDetails()
    context.resource.name = 'Switch for Demo'
    context.resource.address = '192.168.42.235'
    context.resource.attributes = {}
    context.resource.attributes['CLI Connection Type'] = 'SSH'
    context.resource.attributes['User'] = 'root'
    context.resource.attributes['AdminUser'] = 'admin'
    context.resource.attributes['Console Password'] = 'Password1'
    context.resource.attributes['Password'] = 'Password1'
    context.resource.attributes['Enable Password'] = 'Password1'
    context.resource.attributes['Sessions Concurrency Limit'] = 2

    return context

if __name__ == '__main__':
    context = create_context()
    command_modes_list = []
    enable_password = get_attribute_by_name(attribute_name='Enable Password',
                                            context=context)
    expect_map = {'[Pp]assword': lambda session, logger: session.send_line(enable_password, logger)}
    enable_mode = CommandMode(prompt=r'(?:(?!\)).)#\s*$', enter_command='enable', expect_map=expect_map, \
                              commands=['terminal length 0','terminal width 300'])
    command_modes_list.append(enable_mode)
    pool = SessionPoolManager(max_pool_size=1)
    cli = CLI(session_pool=pool)
    cli_handler = SwitchCliHandler(cli, context, logger)

    with cli_handler.get_cli_service(cli_handler.enable_mode) as session:
        session.on_session_start(command_modes_list,logger)
        out = session.send_command('echo checking switch')
        with session.enter_mode(cli_handler.config_mode) as config_session:
            out = config_session.send_command('echo checking switch')
            print (out)
            out = config_session.send_command('echo checking switch')
            print (out)




