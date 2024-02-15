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
        if self.currGear == Gear.NEUTRAL or self.currGear == Gear.REVERSE:
            raise Exception(f"You are in {self.currGear.name}")
        else:
            self.currGear = Gear(self.currGear.value - 1)

    def setNeutral(self):
        self.currGear = Gear.NEUTRAL
        print("You are in Neutral")

    def setReverse(self):
        self.currGear = Gear.REVERSE
        print("You are in Reverse")

    @abstractmethod
    def drive(self):
        pass
