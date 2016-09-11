


class Prompt():

    def __init__(self):
        self.default_prompt = r'.*[>$#]\s*$'
        self.config_mode_promp = r'.*#\s*$'
        self.enable_prompt = '#\s*$'

    def default_prompt(self,prompt_regex):
        self.default_prompt = prompt_regex


    def admin_prompt(self,prompt_regex):
        self.enable_prompt = prompt_regex

    def config_mode_prompt(self,prompt_regex):
        self.enable_prompt=prompt_regex