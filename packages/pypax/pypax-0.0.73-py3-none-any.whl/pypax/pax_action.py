from logkit import log
import os
from typing import Union
from .pypax import Pax


class PaxAction:

    """ A container for an action within a specific repo. """

    def __init__(self, name, commands=None):
        self.name = name
        self.commands = commands
    
    def execute(self, pax: Pax, env_map: Union[dict, None]=None):

        # Join the commands into a full script.
        full_script = "\n".join(self.commands)
        if env_map is not None:
            full_script = self.append_with_environment(full_script, env_map)
        os.system(full_script)

        # Check if results were written to the buffer.
        line = None
        tmp_file = ".tmp_result.txt"
        if os.path.exists(tmp_file):
            with open(tmp_file, "r") as f:
                line = f.readline().strip().replace("\n", "")
            os.remove(tmp_file)
        
        # Print action execution summary.
        self.log_results(self.name, {i: v for i, v in enumerate(self.commands)}, line)

    def log_results(self, name, commands, result):
        log.info("Execution Action", {
            "name": name,
            "commands": commands,
            "result": result
        })

    def append_with_environment(self, script: str, env_map: dict):
        """ Append the environment variables to the script before running it. """
        env_arr = []
        for k, v in env_map.items():
            env_cmd = "{}={};".format(k, v)
            env_arr.append(env_cmd)
        
        env_str = " ".join(env_arr)
        final_command = "{} {}".format(env_str, script)
        return final_command
