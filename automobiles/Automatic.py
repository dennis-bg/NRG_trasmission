import time

from NRG_trasmission.automobiles.Automobile import Automobile
from NRG_trasmission.automobiles.Gear import Gear


def displayNonDriveOptions():
    print(f"{Gear.PARK.name}    : 'p' or 'P'")
    print(f"{Gear.REVERSE.name} : 'r' or 'R'")
    print(f"{Gear.NEUTRAL.name} : 'n' or 'N'")


class Automatic(Automobile):

    def __init__(self, name, noGears, __redLineRevs):
        self.__currRevs = 1500
        self.__redLineRevs = __redLineRevs
        super().__init__(name, noGears)

    def __accelerate(self, targetSpeed):
        while self._currSpeed < targetSpeed and self._currGear.value <= self._noGears:
            print(f"\nCurrent Gear: {self._currGear.name}")
            while self._currSpeed < targetSpeed and self.__currRevs < self.__redLineRevs:
                self.__currRevs += 500
                self._currSpeed += 2
                print(f"Current RPMs  : {self.__currRevs}")
                print(f"Current Speed : {self._currSpeed}")
                time.sleep(0.5)
            try:
                self._upShift()
                self.__currRevs = 1500
            except Exception as e:
                print(e)
                break

    def __decelerate(self, targetSpeed=0):
        while self._currSpeed > targetSpeed and self._currGear.value >= 0:
            print(f"\nCurrent Gear: {self._currGear.name}")
            while self._currSpeed > targetSpeed and self.__currRevs > 2000:
                self.__currRevs -= 1000
                self._currSpeed -= 4
                print(f"Current RPMs  : {self.__currRevs}")
                print(f"Current Speed : {self._currSpeed}")
                time.sleep(0.5)
            try:
                self._downShift()
                self.__currRevs = self.__redLineRevs
            except Exception as e:
                print(e)
                break

    def __setPark(self):
        self._currGear = Gear.PARK

    def _displayOptions(self, inDrive):
        if inDrive:
            print(f"\nCurrent speed : {self._currSpeed} mph\n")
            if self._currSpeed == 0:
                displayNonDriveOptions()
                print("\nChoose a gear to switch to (above) or enter a speed to accelerate to : ", end='')
            else:
                print("What speed would you like to go? : ", end='')
        else:
            print(f"\nCurrent Gear : {self._currGear.name}\n")
            displayNonDriveOptions()
            print("DRIVE   : 'd' or 'D'")
            print(f"QUIT {self._getName()} : 'q' or 'Q'")
            print(f"\nWhat Gear would you like to switch too? (Options Above) : ", end='')

    def __drive(self):
        self._setNeutral()
        self._upShift()
        while self._currGear.value > Gear.NEUTRAL.value:
            self._displayOptions(True)
            speed = int(input())
            if speed < 0:
                print("Speed must be greater than or equal to 0")
            elif speed < self._currSpeed:
                self.__decelerate(speed)
            else:
                self.__accelerate(speed)

    def _handleShiftChange(self, action):
        if action in ['p', 'P']:
            self.__setPark()
        elif action in ['r', 'R']:
            self._setReverse()
        elif action in ['n', 'N']:
            self._setNeutral()
        elif action in ['d', 'D']:
            self.__drive()

    def operate(self):
        action = 'p'
        while action not in ['q', 'Q']:
            self._handleShiftChange(action)
            self._displayOptions(False)
            action = input()


def main():
    automatic_car = Automatic("Toyota", 5, 6000)
    automatic_car.operate()


if __name__ == "__main__":
    main()
