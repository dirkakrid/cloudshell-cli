from abc import ABCMeta, abstractmethod
from cloudshell.cli.service.cli_exceptions import CommandExecutionException
from cloudshell.cli.session.connection_manager import ConnectionManager
from cloudshell.cli.session.session_exceptions import SessionLoopDetectorException, SessionLoopLimitException
from cloudshell.configuration.cloudshell_cli_binding_keys import CONNECTION_MANAGER
from cloudshell.shell.core.config_utils import override_attributes_from_config
import inject


class SessionHolder(object):
    __metaclass__ = ABCMeta

    IGNORED_EXCEPTIONS = [CommandExecutionException, SessionLoopDetectorException, SessionLoopLimitException]

    def __init__(self, session=None, connection_manager=None, config=None):
        self._connection_manager = connection_manager
        self._session = session
        if self._session:
            self._session_defined = True
        else:
            self._session_defined = False
        overridden_config = override_attributes_from_config(ConnectionManager, config=config)
        self._ignored_exceptions = overridden_config.IGNORED_EXCEPTIONS

    @property
    def connection_manager(self):
        """
        :rtype: ConnectionManager
        """
        return self._connection_manager or inject.instance(CONNECTION_MANAGER)


    @abstractmethod
    def __enter__(self):
        pass

    @abstractmethod
    def __exit__(self, exc_type, exc_val, exc_tb):
        pass
