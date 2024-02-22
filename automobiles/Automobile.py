from abc import ABC, abstractmethod

from NRG_trasmission.automobiles.enums.Gear import Gear

# abstract class describing all automobiles
class Automobile(ABC):

    def __init__(self, name, noGears):
        self._currGear = Gear.NEUTRAL
        self._currSpeed = 0
        self._noGears = noGears
        self.__name = name

    # Getters and Setters

    @property
    def name(self):
        return self.__name

    @property
    def noGears(self):
        return self._noGears

    @property
    def currSpeed(self):
        return self._currSpeed

    @currSpeed.setter
    def currSpeed(self, value):
        self._currSpeed = value

    @property
    def currGear(self):
        return self._currGear

    @currGear.setter
    def currGear(self, value):
        self._currGear = value

    # Put the transmission in NEUTRAL or REVERSE for all automobile types

    def _setNeutral(self):
        self._currGear = Gear.NEUTRAL

    def _setReverse(self):
        self._currGear = Gear.REVERSE

    # Shifts the transmission 1 gear up
    # raises an exception if the transmission is in the highest gear
    def _upShift(self):
        if self._currGear.value == self._noGears:
            raise Exception("\nYou are in the highest gear")
        else:
            self._currGear = Gear(self.currGear.value + 1)

    # Shifts the transmission 1 gear down
    # raises an exception if in NEUTRAL or REVERSE
    def _downShift(self):
        if self._currGear in [Gear.NEUTRAL, Gear.REVERSE]:
            raise Exception(f"You are in {self._currGear.name} and cannot down shift")
        else:
            self._currGear = Gear(self.currGear.value - 1)

    # abstract method implemented by concrete classes to handle the user input
    @abstractmethod
    def _handleShiftChange(self, action):
        pass

    # abstract method implemented by concrete classes to display gear shift options
    @abstractmethod
    def _displayOptions(self, inDrive):
        pass

    # abstract method implemented by concrete classes to begin using the automobile
    @abstractmethod
    def operate(self):
        pass
