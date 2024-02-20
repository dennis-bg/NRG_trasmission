from abc import ABC, abstractmethod

from NRG_trasmission.automobiles.Gear import Gear


class Automobile(ABC):

    def __init__(self, name, noGears):
        self._currGear = Gear.NEUTRAL
        self._currSpeed = 0
        self._noGears = noGears
        self.__name = name

    def _getName(self):
        return self.__name

    def _upShift(self):
        if self._currGear.value == self._noGears:
            raise Exception("You are in the highest gear")
        else:
            self._currGear = Gear(self._currGear.value + 1)

    def _downShift(self):
        if self._currGear in [Gear.NEUTRAL, Gear.REVERSE]:
            raise Exception(f"You are in {self._currGear.name} and cannot down shift")
        else:
            self._currGear = Gear(self._currGear.value - 1)

    def _setNeutral(self):
        self._currGear = Gear.NEUTRAL

    def _setReverse(self):
        self._currGear = Gear.REVERSE

    @abstractmethod
    def _handleShiftChange(self, action):
        pass

    @abstractmethod
    def _displayOptions(self, inDrive):
        pass

    @abstractmethod
    def operate(self):
        pass
