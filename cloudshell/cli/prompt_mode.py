from cloudshell.cli.prompt import Prompt
import collections


class Mode(Prompt):

    def __init__(self):


        self.initiate_actions = None

    def _set_actions(self,actions):
        '''
        :param actions: [(action1,prompt),(action2,prompt)...] or (action,prompt)
        :return: None
        '''

        if not isinstance(actions,list) or not isinstance(actions,tuple):
            raise Exception("actions","Actions must be in type of list of nested tuple or a single tuple")
        if isinstance(actions, tuple):
                actions = [actions]
        self.initiate_actions = Actions(actions)

    def enter_mode(self,mode_tuple):pass





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