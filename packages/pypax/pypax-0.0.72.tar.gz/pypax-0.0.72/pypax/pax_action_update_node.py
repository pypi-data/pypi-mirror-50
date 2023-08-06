from .pax_action import PaxAction
import os
from logkit import log
from typing import Union
import re
from .pypax import Pax


class PaxActionUpdateNode(PaxAction):

    def execute(self, pax: Pax, env_map: Union[dict, None]=None):
        
        # Load the node object.
        node_data = pax.load_pax_node_data()
        log.info("Previous Node Data Loaded", node_data)

        # Read the local version.
        old_version = node_data["node"]["version"]
        current_version = pax.load_local_text("version")
        log.info("Read Local Data", {"version": current_version})

        # Update the data version.
        node_data["node"]["version"] = current_version
        log.info("Updated Node Data", node_data)

        # Send the update to the server.
        pax.api_post("update_node", node_data["node"])

        # Save the local config too.
        pax.save_local_object(pax.PAX_NODE_FILE, node_data)

        self.log_results(
            self.name, 
            "<INTERNAL FUNCTION>",
            "Node version was updated: {} -> {}".format(old_version, current_version)
        )
