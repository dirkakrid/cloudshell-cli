from abc import ABCMeta, abstractmethod


class CliOperations(object):
    __metaclass__ = ABCMeta

    def __init__(self):
        self.session = None
        self.command_mode = None

    @abstractmethod
    def send_command(self, command, expected_string=None, *args, **kwargs):
        pass

    @abstractmethod
    def enter_mode(self, command_mode):
        pass
