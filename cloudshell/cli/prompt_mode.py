from cloudshell.cli.prompt import Prompt
import collections


class Mode(Prompt):

    def __init__(self):


        self.initiate_actions = None
        self.modes = None
        self.leave = None

    def _set_actions(self,actions):
        '''
        :param actions: [(action1,prompt),(action2,prompt)...] or (action,prompt)
        :return: None
        '''

        if not isinstance(actions,list) or not isinstance(actions,tuple):
            raise Exception("actions","Actions must be in type of list of nested tuple or a single tuple")
        if isinstance(actions, tuple):
                actions = [actions]
        self.initiate_actions = MutableMapping(actions)

    def enter_mode(self,mode_tuple):pass


    def set_modes(self,modes_tuple):
        '''
        :param modes_tuple: [(action1,prompt),(action2,prompt)...] or (action,prompt)
        :return: None
        '''
        if not isinstance(modes_tuple,list) or not isinstance(modes_tuple,tuple):
            raise Exception("modes","Modes must be in type of list of nested tuple or a single tuple")
        if isinstance(modes_tuple, tuple):
                modes = [modes_tuple]
        self.modes.update(MutableMapping(modes))

    def set_default_mode(self,defualt_mode_tuple):
        if(defualt_mode_tuple!='default'):
            raise Exception("modes", "Default mode name must be default")

        self.modes = MutableMapping(defualt_mode_tuple)

    def exit_mode(self,exit_tuple):
        self.leave =MutableMapping([exit_tuple])


class MutableMapping(collections.MutableMapping):

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


