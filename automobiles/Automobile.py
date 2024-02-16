from abc import ABC, abstractmethod

from NRG_trasmission.automobiles.Gear import Gear


class Automobile(ABC):

    def __init__(self, name, noGears):
        self.currGear = Gear.NEUTRAL
        self.currSpeed = 0
        self.noGears = noGears
        self.name = name

    def upShift(self):
        if self.currGear.value == self.noGears:
            raise Exception("You are in the highest gear")
        else:
            self.currGear = Gear(self.currGear.value + 1)

    def downShift(self):
        if self.currGear in [Gear.NEUTRAL, Gear.REVERSE]:
            raise Exception(f"You are in {self.currGear.name} and cannot down shift")
        else:
            self.currGear = Gear(self.currGear.value - 1)

    def setNeutral(self):
        self.currGear = Gear.NEUTRAL

    def setReverse(self):
        self.currGear = Gear.REVERSE

    @abstractmethod
    def handleShiftChange(self, action):
        pass

    @abstractmethod
    def displayOptions(self):
        pass

    @abstractmethod
    def operate(self):
        pass
