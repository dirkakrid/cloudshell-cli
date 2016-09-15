from cloudshell.cli.Prompt import Prompt
import collections


class Mode():

    def __init__(self):


        self.initiate_actions = None
        self.leave = None
        self.state = None

    def _set_actions(self,actions):
        '''
        :param actions: [(action1,prompt),(action2,prompt)...] or (action,prompt)
        :return: None
        '''

        if not isinstance(actions,list) and not isinstance(actions,tuple):
            raise Exception("actions","Actions must be in type of list of nested tuple or a single tuple")
        if isinstance(actions, tuple):
                actions = [actions]
        self.initiate_actions = MutableMapping(actions)


    def set_different_modes(self,modes_tuple):
        '''
        :param modes_tuple: [(action1,prompt),(action2,prompt)...]
        :return: None
        '''
        states = list()
        prompts = list()
        if not isinstance(modes_tuple,list):
            raise Exception("modes","Modes must be in type of list of nested tuple")
        for mode in modes_tuple:
            states.append(mode[0])
            prompts.append(mode[1])

        self.state = Prompt(states, prompts)


    def get_default_prompt(self):
        try:
            return self.state.default
        except Exception as err:
            raise Exception('Defualt Prompt',"The defualt mode prompt is missing")



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


