import time

from NRG_trasmission.automobiles.Automobile import Automobile
from NRG_trasmission.automobiles.Gear import Gear


def displayNonDriveOptions():
    print(f"{Gear.PARK.name}    : 'p' or 'P'")
    print(f"{Gear.REVERSE.name} : 'r' or 'R'")
    print(f"{Gear.NEUTRAL.name} : 'n' or 'N'")


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
                print(f"Current RPMs  : {self.currRevs}")
                print(f"Current Speed : {self.currSpeed}")
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
                self.currSpeed -= 4
                print(f"Current RPMs  : {self.currRevs}")
                print(f"Current Speed : {self.currSpeed}")
                time.sleep(0.5)
            try:
                self.downShift()
                self.currRevs = self.redLineRevs
            except Exception as e:
                print(e)
                break

    def setPark(self):
        self.currGear = Gear.PARK

    def displayOptions(self, inDrive):
        if inDrive:
            print(f"\nCurrent speed : {self.currSpeed} mph\n")
            if self.currSpeed == 0:
                displayNonDriveOptions()
                print("\nChoose a gear to switch to (above) or enter a speed to accelerate to : ", end='')
            else:
                print("What speed would you like to go? : ", end='')
        else:
            print(f"\nCurrent Gear : {self.currGear.name}\n")
            displayNonDriveOptions()
            print("DRIVE   : 'd' or 'D'")
            print(f"QUIT {self.name} : 'q' or 'Q'")
            print(f"\nWhat Gear would you like to switch too? (Options Above) : ", end='')

    def drive(self):
        self.setNeutral()
        self.upShift()
        while self.currGear.value > Gear.NEUTRAL.value:
            self.displayOptions(True)
            speed = int(input())
            if speed < 0:
                print("Speed must be greater than or equal to 0")
            elif speed < self.currSpeed:
                self.decelerate(speed)
            else:
                self.accelerate(speed)

    def handleShiftChange(self, action):
        if action in ['p', 'P']:
            self.setPark()
        elif action in ['r', 'R']:
            self.setReverse()
        elif action in ['n', 'N']:
            self.setNeutral()
        elif action in ['d', 'D']:
            self.drive()

    def operate(self):
        action = 'p'
        while action not in ['q', 'Q']:
            self.handleShiftChange(action)
            self.displayOptions(False)
            action = input()


def main():
    automatic_car = Automatic("Toyota", 5, 6000)
    automatic_car.operate()


if __name__ == "__main__":
    main()
