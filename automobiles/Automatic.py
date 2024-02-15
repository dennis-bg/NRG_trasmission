from NRG_trasmission.automobiles.Automobile import Automobile


class Automatic(Automobile):

    def __init__(self, name, noGears, redLineRevs):
        self.currRevs = 1500
        self.redLineRevs = redLineRevs
        super().__init__(name, noGears)

    def accelerate(self):
        pass

    def decelerate(self):
        pass

