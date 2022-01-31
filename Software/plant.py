from enum import Enum


class State(Enum):
    HOT = 1
    COLD = 2
    DRAWNING = 3


class Plant():

    def __init__(self, *args, **kwargs):
        """
        Constructor of the plant class
        """

        False