__version__ = "0.0.33"

from .pypax import Pax


def configure():
    Pax.instance().configure()


def initialize():
    Pax.instance().initialize()
