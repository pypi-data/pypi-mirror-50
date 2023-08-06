from .pypax import Pax
from logkit import log
import os
import yaml


# ==========================================================================================
# Public Methods.
# ==========================================================================================


def configure(pax: Pax):
    log.info("Configuring PyPax Singleton!")

    # Create a configuration object.
    config_object = {}

    # Populate it with each of the configs.
    __configure_api_endpoint(pax, config_object)
    __configure_github(config_object)

    # Write the configuration object to disk.
    __write_config(pax, config_object)

    log.info("Pax Configuration Object", config_object)
    log.info("Pax Configuration Results", {
        "success": True,
        "destination": pax.global_config_dst
    })


# ==========================================================================================
# Private Methods.
# ==========================================================================================


def __configure_api_endpoint(pax: Pax, config_object):

    success = False
    while not success:

        # Ask user for the end-point.
        api_endpoint = input("Enter PyPAX Server Endpoint: ")
        log.info("API Endpoint", {"uri": api_endpoint})

        # Test endpoint.
        pax.api_endpoint = api_endpoint
        try:
            success = pax.test_connection()
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


def __configure_github(config_object):
    """ Enter a valid GitHub username and token. """
    github_user = input("Enter GitHub User: ")
    github_pass = input("Enter GitHub Pass: ")
    config_object["github_user"] = github_user
    config_object["github_pass"] = github_pass


def __write_config(pax: Pax, config_object):
    """ Write the configuration object to disk. """
    pax_config_path = pax.global_config_dst
    with open(pax_config_path, "w") as f:
        yaml.dump(config_object, f)
