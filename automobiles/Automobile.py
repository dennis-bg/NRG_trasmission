from abc import ABC, abstractmethod

from NRG_trasmission.automobiles.Gear import Gear


class Automobile(ABC):

    def __init__(self, name, noGears):
        self.currGear = Gear.NEUTRAL
        self.noGears = noGears
        self.name = name

    def upShift(self):
        if self.currGear == self.noGears:
            print("You are in the highest gear")
        else:
            self.currGear = self.currGear + 1

    def downShift(self):
        if self.currGear == Gear.NEUTRAL:
            print("You are in Neutral")
        else:
            self.currGear = self.currGear - 1

    def setNeutral(self):
        self.currGear = Gear.NEUTRAL

    def setReverse(self):
        self.currGear = Gear.REVERSE

    @abstractmethod
    def accelerate(self):
        pass

    @abstractmethod
    def decelerate(self):
        pass
