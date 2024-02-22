from enum import Enum


def inputOptionToString(inputOption):
    return "{name}{space}: '{inputs}'".format(name=inputOption.name, space=' ' * (10 - len(inputOption.name)),
                                              inputs="' or '".join(inputOption.value))


class InputOptions(Enum):
    PARK = ['p', 'P']
    REVERSE = ['r', 'R']
    NEUTRAL = ['n', 'N']
    DRIVE = ['d', 'D']
    UPSHIFT = ['u', 'U']
    DOWNSHIFT = ['d', 'D']
    QUIT = ['q', 'Q']
