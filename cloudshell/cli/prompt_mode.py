from cloudshell.cli.prompt import Prompt
import collections


class Mode(Prompt):

    def __init__(self):

        self.mode = 'default'


    def set_default_actions(self,actions_tuple):
        '''
        :param actions_tuple: (action,prompt)
        :return:
        '''

    def enter_mode(self,mode_tuple):
        pass

    def exit_mode(self,mode_tuple):
        pass




class Actions(collections.MutableMapping):

    def __init__(self, *args, **kwargs):
        self.store = dict()
        self.update(dict(*args, **kwargs))

    def __getitem__(self, key):
        return self.store[self.__keytransform__(key)]

    def __setitem__(self, key, value):
        self.store[self.__keytransform__(key)] = value

    def __delitem__(self, key):
        del self.store[self.__keytransform__(key)]

    def __iter__(self):
        return iter(self.store)

    def __len__(self):
        return len(self.store)

    def __keytransform__(self, key):
        return key