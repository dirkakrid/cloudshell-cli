from cloudshell.cli.cli import CLI
from cloudshell.cli.session_pool_manager import SessionPoolManager
from cloudshell.core.logger.qs_logger import get_qs_logger
from SwitchClihandler import *
from cloudshell.shell.core.context import ResourceCommandContext, ResourceContextDetails, ReservationContextDetails,ConnectivityContext
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


    CommandMode.set_root_mode(DefaultCommandMode)
    CommandMode.set_child_mode(EnableCommandMode)
    CommandMode.set_child_mode(ConfigCommandMode)


    pool = SessionPoolManager(max_pool_size=1)
    cli = CLI(session_pool=pool)
    cli_handler = SwitchCliHandler(cli, context, logger)

    with cli_handler.get_cli_service(cli_handler.enable_mode) as session:
        session.on_session_start(context,logger)
        out = session.send_command('echo checking switch')
        with session.enter_mode(cli_handler.config_mode) as config_session:
            out = config_session.send_command('echo checking switch')
            print (out)
            out = config_session.send_command('echo checking switch')
            print (out)




#{<class 'SwitchClihandler.DefaultCommandMode'>: {<class 'SwitchClihandler.EnableCommandMode'>: {<class 'SwitchClihandler.ConfigCommandMode'>: {}}}}