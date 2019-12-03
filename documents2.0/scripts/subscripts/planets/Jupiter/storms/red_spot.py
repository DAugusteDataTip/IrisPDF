"""This is a test to see how far down Sphinx will search for modules and docstrings.

This is an ode about Jupiter's red spot.
"""


class Planet:
    def __init__(self, name, size):
        self.name = name
        self.size = size

    def distance(self, lightyears):
        """How far is the planet from the sun?"""
        result = lightyears * 5028
        return result

