import time

from NRG_trasmission.automobiles.Automobile import Automobile
from NRG_trasmission.automobiles.Gear import Gear


class Automatic(Automobile):

    def __init__(self, name, noGears, redLineRevs):
        self.currRevs = 1500
        self.redLineRevs = redLineRevs
        super().__init__(name, noGears)

    def accelerate(self, targetSpeed):
        while self.currSpeed < targetSpeed and self.currGear.value <= self.noGears:
            print(f"\nCurrent Gear: {self.currGear.name}")
            while self.currSpeed < targetSpeed and self.currRevs < self.redLineRevs:
                self.currRevs += 500
                self.currSpeed += 2
                print(f"Current Revs: {self.currRevs}")
                print(f"Current Speed: {self.currSpeed}")
                time.sleep(0.5)
            try:
                self.upShift()
                self.currRevs = 1500
            except Exception as e:
                print(e)
                break

    def decelerate(self, targetSpeed=0):
        while self.currSpeed > targetSpeed and self.currGear.value >= 0:
            print(f"\nCurrent Gear: {self.currGear.name}")
            while self.currSpeed > targetSpeed and self.currRevs > 2000:
                self.currRevs -= 1000
                self.currSpeed -= 5
                print(f"Current Revs: {self.currRevs}")
                print(f"Current Speed: {self.currSpeed}")
                time.sleep(0.5)
            try:
                self.downShift()
                self.currRevs = self.redLineRevs
            except Exception as e:
                print(e)
                break

    def drive(self):
        self.currGear = Gear.FIRST
        self.accelerate(45)
        self.decelerate(10)


def main():
    automatic_car = Automatic("Toyota", 5, 6000)
    print("Starting acceleration...")
    automatic_car.drive()
    print("Acceleration finished.")


if __name__ == "__main__":
    main()
