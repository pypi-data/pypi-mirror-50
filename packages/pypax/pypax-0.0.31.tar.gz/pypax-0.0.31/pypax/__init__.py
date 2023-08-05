__version__ = "0.0.31"

from .pypax import Pax


def configure():
    Pax.instance().configure()


def initialize():
    Pax.instance().initialize()
