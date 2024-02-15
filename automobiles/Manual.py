from NRG_trasmission.automobiles.Automobile import Automobile


class Manual(Automobile):

    def __init__(self, name, noGears):
        Automobile.__init__(name, noGears)

    def setGear(self, gear):
        self.currGear = gear

    def accelerate(self):
        pass

    def decelerate(self):
        pass
