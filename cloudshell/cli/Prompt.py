


class Prompt(object):

    def __init__(self, keys, values):

        for (key, value) in zip(keys, values):
            self.__dict__[key] = value

        self.default_prompt = r'.*[>$#]\s*$'
        self.config_mode_promp = r'.*#\s*$'
        self.enable_prompt = '#\s*$'
        self.current_prompt_regex = ''



    def __setattr__(self, name, value):
        pass

    def default_prompt(self,prompt_regex):
        self.default_prompt = prompt_regex


    def current_prompt(self,prompt_regex):
        self.current_prompt_regex = prompt_regex

