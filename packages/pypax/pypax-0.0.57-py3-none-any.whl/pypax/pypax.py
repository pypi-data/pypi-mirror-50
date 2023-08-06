import os
import requests
from logkit import log
import yaml


class Pax:
    
    PAX_ROOT           = ".pax/"
    PAX_CONFIG_DIR     = "~/.config/pax"
    PAX_NODE_FILE      = "pax_node.yml"
    PAX_ACTIONS_FILE   = "pax_actions.yml"
    GLOBAL_CONFIG_FILE = "pax_config.yml"

    INSTANCE = None

    @classmethod
    def instance(cls):
        if cls.INSTANCE is None:
            cls.INSTANCE = Pax()
        return cls.INSTANCE

    def __init__(self):
        self.api_endpoint = "http://google.com"
        log.info("Pax Singleton Initialized")

        try:
            data = self.__read_global_config()
            self.api_endpoint = data["api_endpoint"]
            log.info("Global Config Data Loaded", data)

        except Exception as e:
            log.info("Global Config not found. Please pax configure.", 
            {
                "error": str(e)
            })

    # ==========================================================================================
    # Public Methods
    # ==========================================================================================

    @staticmethod
    def get_remote_git_branch():
        process = os.popen('git config --get remote.origin.url')
        remote_origin = process.read()
        process.close()
        remote_url = remote_origin.replace(".git", "").strip().replace("\n", "")
        return remote_url

    # ==========================================================================================
    # File IO.
    # ==========================================================================================

    def ensure_and_join(self, directory: str, path: str):
        """ Expand the directory, ensure it exists, and join the path. """
        expanded_dir = os.path.expanduser(directory)
        os.makedirs(expanded_dir, exist_ok=True)
        full_path = os.path.join(expanded_dir, path)
        return full_path

    def load_local_object(self, path):
        object_file = self.ensure_and_join(self.PAX_ROOT, path)
        object_data = None
        if os.path.exists(object_file):
            with open(object_file, "r") as f:
                object_data = yaml.load(f)
        return object_data

    def save_local_object(self, path, data):
        object_file = self.ensure_and_join(self.PAX_ROOT, path)
        with open(object_file, "w") as f:
            yaml.dump(data, f)

    def load_pax_node_data(self):
        return self.load_local_object(self.PAX_NODE_FILE)

    def load_pax_actions_data(self):
        return self.load_local_object(self.PAX_ACTIONS_FILE)
    
    @property
    def node_data_dst(self):
        return self.ensure_and_join(self.PAX_ROOT, self.PAX_NODE_FILE)

    @property
    def actions_data_dst(self):
        return self.ensure_and_join(self.PAX_ROOT, self.PAX_ACTIONS_FILE)

    @property
    def global_config_dst(self):
        return self.ensure_and_join(self.PAX_CONFIG_DIR, self.GLOBAL_CONFIG_FILE)
  
    # ==========================================================================================
    # Server Comm. Methods.
    # ==========================================================================================

    def test_connection(self):
        status, response, data = self.api_get("")
        log.info("Response", {
            "status": status,
            "content": response.text
        })
        
        # Was the connection a success?
        # TODO: Add some other verification. Status might not be enough.
        return status == 200

    def get_tags(self):
        """ Get a list of package codes from the server. """
        _, _, data = self.api_get("get_nodes")
        nodes = data["nodes"]
        tags = {node["tag"] for node in nodes}
        log.info("Tags", tags)
        return tags

    def add_node_to_server(self, node):
        self.api_post("add_node", node)

    def api_get(self, route=""):
        endpoint = f"{self.api_endpoint}/{route}"
        print(f"Get Front Route: {endpoint}")
        response = requests.get(endpoint)
        return self.__spread(response)

    def api_post(self, route="", data={}):
        endpoint = f"{self.api_endpoint}/{route}"
        response = requests.post(endpoint, json=data)
        return self.__spread(response)

    def __spread(self, response):
        status = response.status_code
        try:
            data = response.json()
        except Exception as _:
            data = None
        return status, response, data

    # ==========================================================================================
    # Support Methods.
    # ==========================================================================================

    def __read_global_config(self):

        pax_config_path = self.global_config_dst
        log.info("Loading Config Path", {
            "path": pax_config_path
        })

        with open(pax_config_path, "r") as f:
            data = yaml.load(f)

        log.info("Local Config Loaded", {
            "path": pax_config_path,
            "data": data
        })

        return data
