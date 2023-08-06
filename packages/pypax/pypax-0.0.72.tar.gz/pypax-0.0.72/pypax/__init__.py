__version__ = "0.0.72"

from .pypax import Pax
from . import pax_deploy
from . import pax_global
from . import pax_initialize


def instance():
    return Pax.instance()


def configure():
    pax_global.configure(instance())


def initialize():
    pax_initialize.initialize(instance())


def deploy(tag: str="default"):
    pax_deploy.deploy(instance(), tag)
