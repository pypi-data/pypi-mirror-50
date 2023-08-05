__version__ = "0.0.38"

from .pypax import Pax


def configure():
    Pax.instance().configure()


def initialize():
    Pax.instance().initialize()
