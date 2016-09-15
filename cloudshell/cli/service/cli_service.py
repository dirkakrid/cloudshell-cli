import time
import traceback

from types import ModuleType
from cloudshell.cli.service.cli_service_interface import CliServiceInterface
from cloudshell.cli.service.cli_exceptions import CommandExecutionException
from cloudshell.cli.session.session_exceptions import SessionLoopDetectorException, SessionLoopLimitException
from cloudshell.shell.core.config_utils import override_attributes_from_config
import cloudshell.configuration.cloudshell_cli_configuration as package_config
from cloudshell.configuration.cloudshell_cli_binding_keys import SESSION, CONNECTION_MANAGER
from cloudshell.configuration.cloudshell_shell_core_binding_keys import CONFIG, LOGGER
import re
import inject


class CliService(CliServiceInterface):
    #EXPECTED_MAP = package_config.EXPECTED_MAP
    #ERROR_MAP = package_config.ERROR_MAP
    #COMMAND_RETRIES = package_config.COMMAND_RETRIES
    #DEFAULT_PROMPT = package_config.DEFAULT_PROMPT
    #CONFIG_MODE_PROMPT = package_config.CONFIG_MODE_PROMPT
    #ENTER_CONFIG_MODE_PROMPT_COMMAND = package_config.ENTER_CONFIG_MODE_PROMPT_COMMAND
    #EXIT_CONFIG_MODE_PROMPT_COMMAND = package_config.EXIT_CONFIG_MODE_PROMPT_COMMAND
    #COMMIT_COMMAND = package_config.COMMIT_COMMAND
    #ROLLBACK_COMMAND = package_config.ROLLBACK_COMMAND

    def __init__(self, use_config=False,config=None, logger=None):
        self._config = config
        self._logger = logger
        if use_config:
            """Override constants with global config values"""
            overridden_config = override_attributes_from_config(CliService, config=self.config)
            self._expected_map = overridden_config.EXPECTED_MAP
            self._error_map = overridden_config.ERROR_MAP
            self._command_retries = overridden_config.COMMAND_RETRIES
            self._prompt = overridden_config.DEFAULT_PROMPT
            self._config_mode_prompt = overridden_config.CONFIG_MODE_PROMPT
            self._enter_config_mode_prompt_command = overridden_config.ENTER_CONFIG_MODE_PROMPT_COMMAND
            self._exit_config_mode_prompt_command = overridden_config.EXIT_CONFIG_MODE_PROMPT_COMMAND
            self._commit_command = overridden_config.COMMIT_COMMAND
            self._rollback_command = overridden_config.ROLLBACK_COMMAND

    @property
    def config(self):
        """
        Property for config
        :rtype: ModuleType
        """
        if self._config:
            config = self._config
        elif inject.is_configured():
            config = inject.instance(CONFIG)
        else:
            config = ModuleType('config')
        return config

    @property
    def logger(self):
        """
        Property for the logger
        :rtype: Logger
        """
        return self._logger or inject.instance(LOGGER)

    @logger.setter
    def logger(self, logger):
        self._logger = logger

    @inject.params(session=SESSION)
    def get_session_type(self, session):
        return session.session_type

    @inject.params(session=SESSION)
    def send_config_command(self, command, expected_str=None, expected_map=None, error_map=None,
                            session=None, **optional_args):
        """Send command into configuration mode, enter to config mode if needed
        :param command: command to send
        :param expected_str: expected output string (_prompt by default)
        :return: received output buffer
        """

        self._enter_configuration_mode(session)

        if expected_str is None:
            expected_str = self._config_mode_prompt

        out = self._send_command(command, expected_str, expected_map=expected_map, error_map=error_map, session=session,
                                 **optional_args)
        # logger.info(out)
        return out

    @inject.params(session=SESSION)
    def send_command(self, command, expected_str=None, expected_map=None, error_map=None, session=None,
                     **optional_args):
        """Send command in default mode

        :param command: command to send
        :param expected_str: expected output string (_prompt by default)
        :param expected_map: action map (string - action)
        :param logger:
        :param session:
        :return: received output buffer
        """

        self.exit_configuration_mode(session=session)
        try:
            out = self._send_command(command, expected_str=expected_str, expected_map=expected_map, error_map=error_map,
                                     session=session, **optional_args)
        except CommandExecutionException as e:
            self.rollback()
            self.logger.error(e)
            raise e
        return out

    def _send_command(self, command, expected_str=None, expected_map=None, error_map=None, session=None,
                      is_need_default_prompt=True, command_retries=None, **optional_args):
        """Send command

        :param command: command to send
        :param expected_str: expected output string (_prompt by default)
        :param timeout: command timeout
        :return: received output buffer
        """

        if not expected_map:
            expected_map = self._expected_map

        if not error_map:
            error_map = self._error_map

        if not expected_str:
            expected_str = self._prompt
        else:
            if is_need_default_prompt:
                expected_str = expected_str + '|' + self._prompt

        command_retries_count = self._command_retries
        if command_retries:
            command_retries_count = command_retries

        out = ''
        for retry in range(command_retries_count):
            try:
                out = session.hardware_expect(command, expected_str, expect_map=expected_map, error_map=error_map,
                                              **optional_args)
                break
            except (CommandExecutionException, SessionLoopDetectorException, SessionLoopLimitException):
                raise
            except Exception as e:
                self.logger.error(e)
                if retry == command_retries - 1:
                    self.logger.error(traceback.format_exc())
                    raise Exception('Failed to send command')
                session.reconnect(self._prompt)
        return out

    def send_command_list(self, commands_list, send_command_func=None, expected_map=None, error_map=None,
                          **optional_args):
        output = ""
        if not send_command_func:
            send_command_func = self.send_config_command
        for command in commands_list:
            output += send_command_func(command=command, expected_map=expected_map, error_map=error_map,
                                        **optional_args)
        return output

    @inject.params(session=SESSION)
    def exit_configuration_mode(self, session=None, **optional_args):
        """Send 'enter' to SSH console to get prompt,
        if config prompt received , send 'exit' command, change _prompt to DEFAULT
        else: return

        :return: console output
        """

        out = None
        for retry in range(5):
            out = self._send_command(' ', expected_str=self._prompt + "|" + self._config_mode_prompt, session=session,
                                     **optional_args)
            if re.search(self._config_mode_prompt, out):
                self._send_command(self._exit_config_mode_prompt_command,
                                   expected_str=self._prompt + "|" + self._config_mode_prompt, session=session,
                                   **optional_args)
            else:
                break

        return out

    @inject.params(session=SESSION)
    def _enter_configuration_mode(self, session=None, **optional_args):
        """Send 'enter' to SSH console to get prompt,
        if default prompt received , send 'configure terminal' command, change _prompt to CONFIG_MODE
        else: return

        :return: True if config mode entered, else - False
        """

        out = None
        for retry in range(3):
            out = self._send_command(' ', expected_str=self._prompt + "|" + self._config_mode_prompt, session=session,
                                     **optional_args)
            if not out:
                self.logger.error('Failed to get prompt, retrying ...')
                time.sleep(1)

            elif not re.search(self._config_mode_prompt, out):
                out = self._send_command(self._enter_config_mode_prompt_command, self._config_mode_prompt,
                                         session=session, **optional_args)
                # if( re.search(self._config_mode_prompt, out)): break

            else:
                break

        if not out:
            return False
        # self._prompt = self.CONFIG_MODE_PROMPT
        return re.search(self._prompt, out)

    def commit(self, expected_map=None):
        self.send_config_command(self._commit_command, expected_map=expected_map)

    def rollback(self, expected_map=None):
        self.send_config_command(self._rollback_command, expected_map=expected_map)

    @inject.params(session=SESSION, cm=CONNECTION_MANAGER)
    def destroy_threaded_session(self, session=None, logger=None, cm=None):
        """

        :param session:
        :param logger:
        :return:
        """
        logger.info('Closing session ....')
        cm.destroy_thread_session(session)
