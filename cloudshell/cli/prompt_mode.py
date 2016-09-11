from cloudshell.cli.prompt import Prompt

class Prompt_Mode(Prompt):

    def __init__(self):
        self.default_actions = list()


    def default_actions(self,actions_tuple):
        '''
        :param actions_tuple: (action,prompt)
        :return:
        '''