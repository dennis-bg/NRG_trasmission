from abc import ABC, abstractmethod

from NRG_trasmission.automobiles.Gear import Gear


class Automobile(ABC):

    def __init__(self, name, noGears):
        self._currGear = Gear.NEUTRAL
        self._currSpeed = 0
        self._noGears = noGears
        self.__name = name

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

    def _setNeutral(self):
        self._currGear = Gear.NEUTRAL

    def _setReverse(self):
        self._currGear = Gear.REVERSE

    def _upShift(self):
        if self._currGear.value == self._noGears:
            raise Exception("You are in the highest gear")
        else:
            self._currGear = Gear(self.currGear.value + 1)

    def _downShift(self):
        if self._currGear in [Gear.NEUTRAL, Gear.REVERSE]:
            raise Exception(f"You are in {self._currGear.name} and cannot down shift")
        else:
            self._currGear = Gear(self.currGear.value - 1)

    @abstractmethod
    def _handleShiftChange(self, action):
        pass

    @abstractmethod
    def _displayOptions(self, inDrive):
        pass

    @abstractmethod
    def operate(self):
        pass
