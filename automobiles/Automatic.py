import time

from NRG_trasmission.automobiles.Automobile import Automobile
from NRG_trasmission.automobiles.Gear import Gear, getAcceleration


def displayNonDriveOptions():
    print(f"{Gear.PARK.name}    : 'p' or 'P'")
    print(f"{Gear.REVERSE.name} : 'r' or 'R'")
    print(f"{Gear.NEUTRAL.name} : 'n' or 'N'")


class Automatic(Automobile):

    def __init__(self, name, noGears, redLineRevs):
        self._currRevs = 1500
        self._redLineRevs = redLineRevs
        super().__init__(name, noGears)

    def _setPark(self):
        self.currGear = Gear.PARK

    def _accelerate(self, targetSpeed):
        while self.currSpeed < targetSpeed:
            print(f"\nCurrent Gear  : {self.currGear.name}")
            while self.currSpeed < targetSpeed and self._currRevs < self._redLineRevs:
                self._currRevs += 500
                self.currSpeed = min(self.currSpeed + getAcceleration(self.currGear), targetSpeed)
                print(f"Current RPMs  : {self._currRevs}")
                print(f"Current Speed : {int(self._currSpeed)}")
                time.sleep(0.1)
            if self.currSpeed != targetSpeed:
                try:
                    self._upShift()
                    self._currRevs = 1500
                except Exception as e:
                    print(f"{e}, cannot accelerate anymore")
                    return

    def _decelerate(self, targetSpeed=0):
        while self.currSpeed > targetSpeed and self.currGear.value >= 0:
            print(f"\nCurrent Gear  : {self.currGear.name}")
            while self.currSpeed > targetSpeed and self._currRevs > 1500:
                self._currRevs -= 500
                self.currSpeed = max(self.currSpeed - getAcceleration(self.currGear), targetSpeed)
                print(f"Current RPMs  : {self._currRevs}")
                print(f"Current Speed : {int(self._currSpeed)}")
                time.sleep(0.5)
            if self.currSpeed != targetSpeed:
                try:
                    self._downShift()
                    self._currRevs = self._redLineRevs
                except Exception as e:
                    print(e)
                    break

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
        self._currRevs = 1500
        validInputs = ['p', 'P', 'n', 'N', 'r', 'R']
        while True:
            self._displayOptions(True)
            inputSpeed = input()
            if not inputSpeed.isnumeric():
                if inputSpeed in validInputs:
                    return inputSpeed
                else:
                    print("\nNot a valid input")
                    continue
            targetSpeed = int(inputSpeed)
            if targetSpeed < 0:
                print("Speed must be greater than or equal to 0")
            elif targetSpeed < self.currSpeed:
                self._decelerate(targetSpeed)
            else:
                self._accelerate(targetSpeed)

    def _handleShiftChange(self, action):
        if action in ['p', 'P']:
            self._setPark()
            return None
        elif action in ['r', 'R']:
            self._setReverse()
            return None
        elif action in ['n', 'N']:
            self._setNeutral()
            return None
        elif action in ['d', 'D']:
            return self._drive()

    def operate(self):
        action = 'p'
        while action not in ['q', 'Q']:
            shiftFromDrive = self._handleShiftChange(action)
            if shiftFromDrive is not None:
                self._handleShiftChange(shiftFromDrive)
            self._displayOptions(False)
            action = input()


def main():
    automatic_car = Automatic("Toyota", 6, 6000)
    automatic_car.operate()


if __name__ == "__main__":
    main()
