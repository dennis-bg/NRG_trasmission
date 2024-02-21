import time

from NRG_trasmission.automobiles.Automobile import Automobile
from NRG_trasmission.automobiles.Gear import Gear, getAcceleration


def displayNonDriveOptions():
    print(f"{Gear.PARK.name}    : 'p' or 'P'")
    print(f"{Gear.REVERSE.name} : 'r' or 'R'")
    print(f"{Gear.NEUTRAL.name} : 'n' or 'N'")


class Automatic(Automobile):

    def __init__(self, name, noGears, redLineRevs):
        self.__currRevs = 1500
        self.__redLineRevs = redLineRevs
        super().__init__(name, noGears)

    def _accelerate(self, targetSpeed):
        while self.currSpeed < targetSpeed:
            print(f"\nCurrent Gear: {self.currGear.name}")
            while self.currSpeed < targetSpeed and self.__currRevs < self.__redLineRevs:
                self.__currRevs += 500
                self.currSpeed = min(self.currSpeed + getAcceleration(self.currGear), targetSpeed)
                print(f"Current RPMs  : {self.__currRevs}")
                print(f"Current Speed : {int(self._currSpeed)}")
                time.sleep(0.5)
            if self.currSpeed != targetSpeed:
                try:
                    self._upShift()
                    self.__currRevs = 1500
                except Exception as e:
                    print(f"{e}, cannot accelerate anymore")
                    return

    def _decelerate(self, targetSpeed=0):
        while self.currSpeed > targetSpeed and self.currGear.value >= 0:
            print(f"\nCurrent Gear : {self.currGear.name}")
            while self.currSpeed > targetSpeed and self.__currRevs > 1500:
                self.__currRevs -= 500
                self.currSpeed = max(self.currSpeed - getAcceleration(self.currGear), targetSpeed)
                print(f"Current RPMs  : {self.__currRevs}")
                print(f"Current Speed : {int(self._currSpeed)}")
                time.sleep(0.5)
            if self.currSpeed != targetSpeed:
                try:
                    self._downShift()
                    self.__currRevs = self.__redLineRevs
                except Exception as e:
                    print(e)
                    break

    def _setPark(self):
        self.currGear = Gear.PARK

    def _displayOptions(self, inDrive):
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

    def _drive(self):
        self._setNeutral()
        self._upShift()
        self.__currRevs = 1500
        while input not in ['p', 'P', 'n', 'N', 'r', 'R']:
            self._displayOptions(True)
            speed = int(input())
            if speed < 0:
                print("Speed must be greater than or equal to 0")
            elif speed < self.currSpeed:
                self._decelerate(speed)
            else:
                self._accelerate(speed)

    def _handleShiftChange(self, action):
        if action in ['p', 'P']:
            self._setPark()
        elif action in ['r', 'R']:
            self._setReverse()
        elif action in ['n', 'N']:
            self._setNeutral()
        elif action in ['d', 'D']:
            self._drive()

    def operate(self):
        action = 'p'
        while action not in ['q', 'Q']:
            self._handleShiftChange(action)
            self._displayOptions(False)
            action = input()


def main():
    automatic_car = Automatic("Toyota", 6, 6000)
    automatic_car.operate()


if __name__ == "__main__":
    main()
