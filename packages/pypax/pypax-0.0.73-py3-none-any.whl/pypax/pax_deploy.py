# Execute all actions to 'deploy' this repo.
from .pypax import Pax
from logkit import log
from .pax_action import PaxAction
import os
import yaml

# ==========================================================================================
# Import built-in actions.
# ==========================================================================================

from .pax_action_modify_helm_image import PaxActionModifyHelmImage
from .pax_action_update_node import PaxActionUpdateNode

# ==========================================================================================
# Constants.
# ==========================================================================================

TAG_DEFAULT = "default"

# ==========================================================================================
# Methods.
# ==========================================================================================


def deploy(pax: Pax, tag: str="staging"):

    actions = load_actions(pax)
    steps = load_deployment(pax, tag)
    env_map = load_environment_config(pax, tag)

    for i, key in enumerate(steps):
        if key not in actions:
            log.warning("Action not found", {
                "step_i": i,
                "action_key": key
            })
            break
        
        action = actions[key]
        action.execute(pax, env_map)


def load_environment_config(pax: Pax, tag: str="default"):

    # Load the default environment map first.
    pax_data = pax.load_pax_actions_data()
    deploy_data = pax_data["deploy"]
    env_map = deploy_data[TAG_DEFAULT]["config"]  # Load the default.

    # Update/override the environment map with values from the overarching directive.
    if tag in deploy_data and tag != TAG_DEFAULT:
        tag_env_map = deploy_data[tag]["config"]
        for k, v in tag_env_map.items():
            env_map[k] = v

    # Updated env map.
    log.info("Loaded ENV Config", env_map)
    return env_map


def load_actions(pax: Pax):
    """ Load all the valid actions that can be deployed. """

    # Start with the hard-coded actions.
    actions = __load_hard_coded_actions()

    # Load action definitions from the yaml.
    actions_map = pax.load_pax_actions_data()["actions"]
    if actions_map is None:
        log.warning("No actions found.", {"path": "actions.yml"})

    # Link each action.
    for k, v in actions_map.items():
        action = PaxAction(k, v)
        actions[k] = action
    
    # Return the final map.
    return actions


def __load_hard_coded_actions():
    """ Load hard-coded Python actions into the map. """
    actions = {
        "modify_helm_image": PaxActionModifyHelmImage("modify_helm_image"),
        "update_node_on_server": PaxActionUpdateNode("update_node_on_server")
    }
    return actions


def load_deployment(pax: Pax, deploy_tag: str):
    """ Load all the saved actions from this Pax instance. """

    # Get the deployment object from the PAX yaml.
    deploy_map = pax.load_pax_actions_data()["deploy"]
    steps = []

    if deploy_map is None:
        log.warning("No actions found.", {"path": pax.actions_data_dst})
    else:
        log.info("Deployment Object Loaded", deploy_map)
        steps = deploy_map[deploy_tag]["steps"]

    return steps
