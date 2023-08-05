# -*- coding: utf-8 -*-

"""
Holds all the structured data for this package.
"""


class PaxData:
    def __init__(self):
        self.tag = "AAA"  # Unique tag to use for this pax package.
        self.inbound = []  # List of tags required for this package.
        self.version = "0.0.0"

    def load(self):
        pass

    def save(self):
        pass
