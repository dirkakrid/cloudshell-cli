from cloudshell.cli.service.cli_exceptions import CommandExecutionException
from cloudshell.cli.session.session_exceptions import SessionLoopDetectorException, SessionLoopLimitException
from cloudshell.cli.session.session_holder import SessionHolder
from cloudshell.configuration.cloudshell_cli_binding_keys import CONNECTION_MANAGER
from cloudshell.cli.session.connection_manager import ConnectionManager
from cloudshell.shell.core.config_utils import override_attributes_from_config
import inject


class SessionFromPoolHolder(SessionHolder):

    def __enter__(self):
        if not self._session:
            self._session = self.connection_manager.get_session_instance()
        return self._session

    def __exit__(self, exc_type, exc_val, exc_tb):
        if not exc_type or exc_type in self._ignored_exceptions:
            if self._session and not self._session_defined:
                self.connection_manager.return_session_to_pool(self._session)
                self._session = None
        else:
            if self._session and not self._session_defined:
                self.connection_manager.decrement_sessions_count()
