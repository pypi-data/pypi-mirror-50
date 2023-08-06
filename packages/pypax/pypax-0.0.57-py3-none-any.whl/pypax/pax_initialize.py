from .pypax import Pax
from logkit import log
import os
import yaml
import shutil


# ==========================================================================================
# Public Methods.
# ==========================================================================================

def initialize(pax: Pax):
    """ Initialize this path as a PyPAX source. """

    log.info("Initializing Repo as PAX package!")
    tag = __enter_verified_tag(pax)
    description = input("Enter package description: ")
    link = pax.get_remote_git_branch()

    node = {
        "tag": tag,
        "inbound": [],
        "version": "0.0.0",
        "description": description,
        "link": link
    }

    node_data = {
        "node": node
    }

    log.info("Node Created", node)

    pax.add_node_to_server(node)
    pax.save_local_object(pax.PAX_NODE_FILE, node_data)
    __clone_default_actions(pax)

    log.info("Added to server")


# ==========================================================================================
# Private Methods.
# ==========================================================================================


def __enter_verified_tag(pax: Pax):
    """ User enters a tag until they find one that is verified. """

    server_tags = pax.get_tags()

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


def __clone_default_actions(pax: Pax):
    """ PyPAX comes bundled with a default pax_actions.yml. Clone this into the local repo. """
    dir_path = os.path.dirname(os.path.realpath(__file__))
    print(dir_path)
    actions_file = os.path.join(dir_path, "pax_actions.yml")
    shutil.copy(actions_file, pax.actions_data_dst)
    