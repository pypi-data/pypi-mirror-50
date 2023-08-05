__version__ = "0.0.43"

from .pypax import Pax


def configure():
    Pax.instance().configure()


def initialize():
    Pax.instance().initialize()


def instance():
    return Pax.instance()
