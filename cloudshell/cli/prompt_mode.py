from cloudshell.cli.prompt import Prompt

class Mode(Prompt):

    def __init__(self):
        self.default_actions = list()


    def default_actions(self,actions_tuple):
        '''
        :param actions_tuple: (action,prompt)
        :return:
        '''


    def enter_mode(self):
        pass

    def exit_mode(self):
        pass

