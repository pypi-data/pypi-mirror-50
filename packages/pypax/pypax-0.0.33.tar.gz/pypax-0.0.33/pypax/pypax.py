import os
import requests
from logkit import log
import yaml


class Pax:
    
    PAX_ROOT = ".pax/"
    PAX_CONFIG_DIR = "~/.config/pax"
    INSTANCE = None

    @classmethod
    def instance(cls):
        if cls.INSTANCE is None:
            cls.INSTANCE = Pax()
        return cls.INSTANCE

    def __init__(self):
        self.api_endpoint = "http://pax.genvis.co/api/v1"

    # ==========================================================================================
    # Public Methods
    # ==========================================================================================
    
    def configure(self):
        log.info("Configuring PyPax Singleton!")

        # Create a configuration object.
        config_object = {}

        # Populate it with each of the configs.
        self.__configure_api_endpoint(config_object)
        self.__configure_github(config_object)

        # Write the configuration object to disk.
        self.__write_config(config_object)

        log.info("Pax Configuration Object", config_object)

        log.info("Pax Configuration Results", {
            "success": True,
            "destination": self.__config_file_dst
        })

    def initialize(self):
        """ Initialize this path as a PyPAX source. """
        log.info("Initializing Repo as PAX package!")
        tag = self.__enter_verified_tag()
        description = input("Enter package description: ")
        link = input("Enter package URL (GitHub): ")

        node = {
            "tag": tag,
            "inbound": [],
            "version": "0.0.0",
            "description": description,
            "link": link
        }

        pax_object = {
            "node": node
        }

        self.__add_node_to_server(node)
        self.__write_node_config(pax_object)
        log.info("Node Created", node)

    def test_connection(self):
        status, response, data = self.__api_get("")
        log.info("Response", {
            "status": status,
            "content": response.text
        })
        
        # Was the connection a success?
        # TODO: Add some other verification. Status might not be enough.
        return status == 200

    # ==========================================================================================
    # Private: Initialization.
    # ==========================================================================================
    
    def __enter_verified_tag(self):
        """ User enters a tag until they find one that is verified. """

        server_tags = self.__get_tags()

        while True:
            tag = input("Enter 3-letter tag for this package: ")

            if len(tag) != 3:
                log.warning("Tag must be 3 characters!", {
                    "invalid_tag": tag
                })
                continue

            tag = tag[:3].upper()

            if tag in server_tags:
                log.warning("Tag already exists on the server! Please enter a different tag.", {
                    "invalid_tag": tag
                })
                continue

            break

        return tag

    def __write_node_config(self, config_object):
        # Otherwise install new pax script.
        pax_config_path = self.__node_config_dst
        with open(pax_config_path, "w") as f:
            yaml.dump(config_object, f)

    @property
    def __node_config_dst(self):
        # Ensure the configuration directory exists.
        pax_config_dir = os.path.expanduser(self.PAX_ROOT)
        os.makedirs(pax_config_dir, exist_ok=True)
        return os.path.join(pax_config_dir, "pax.yml")

    # ==========================================================================================
    # Private: Configuration.
    # ==========================================================================================

    def __configure_api_endpoint(self, config_object):

        success = False
        while not success:

            # Ask user for the end-point.
            api_endpoint = input("Enter PyPAX Server Endpoint: ")
            log.info("API Endpoint", {"uri": api_endpoint})

            # Test endpoint.
            self.api_endpoint = api_endpoint
            try:
                success = self.test_connection()
            except Exception as e:
                log.warning("Unable to connect to endpoint", {
                    "endpoint": api_endpoint,
                    "error": str(e)
                })

            if success:
                # Add the API enpoint to the configuration object.
                config_object["api_endpoint"] = api_endpoint
            else:
                log.warning("This API Endpoint failed to connect.")

    def __configure_github(self, config_object):
        """ Enter a valid GitHub username and token. """
        github_user = input("Enter GitHub User: ")
        github_pass = input("Enter GitHub Pass: ")
        config_object["github_user"] = github_user
        config_object["github_pass"] = github_pass

    def __write_config(self, config_object):
        """ Write the configuration object to disk. """
        # Write configuration to yaml.
        pax_config_path = self.__config_file_dst
        with open(pax_config_path, "w") as f:
            yaml.dump(config_object, f)

    @property
    def __config_file_dst(self):
        # Ensure the configuration directory exists.
        pax_config_dir = os.path.expanduser(self.PAX_CONFIG_DIR)
        os.makedirs(pax_config_dir, exist_ok=True)
        return os.path.join(pax_config_dir, "pax_config.yml")
        
    # ==========================================================================================
    # Private: General
    # ==========================================================================================

    def __get_tags(self):
        """ Get a list of package codes from the server. """
        _, _, data = self.__api_get("get_nodes")
        nodes = data["nodes"]
        tags = {node["tag"] for node in nodes}
        log.info("Tags", tags)
        return tags

    def __add_node_to_server(self, node):
        self.__api_post("add_node", node)

    def __api_get(self, route=""):
        endpoint = f"{self.api_endpoint}/{route}"
        print(f"Get Front Route: {endpoint}")
        response = requests.get(endpoint)
        return self.__spread(response)

    def __api_post(self, route="", data={}):
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
