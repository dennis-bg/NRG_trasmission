import math
from enum import Enum


def getAcceleration(gear):
    denominator = gear.value if gear != Gear.NEUTRAL else 1
    return (2 / denominator) + (gear.value // 3)


def gearToString(gear):
    return f"{gear.name}{' ' * (10 - len(gear.name))}: '{gear.value}'"


class Gear(Enum):
    PARK = -2
    REVERSE = -1
    NEUTRAL = 0
    FIRST = 1
    SECOND = 2
    THIRD = 3
    FOURTH = 4
    FIFTH = 5
    SIXTH = 6
    SEVENTH = 7
    EIGHTH = 8
    NINTH = 9
    TENTH = 10
