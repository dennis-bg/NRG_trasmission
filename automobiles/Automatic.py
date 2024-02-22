import time

from NRG_trasmission.automobiles.Automobile import Automobile
from NRG_trasmission.automobiles.enums.Gear import Gear, getAcceleration
from NRG_trasmission.automobiles.enums.InputOptions import InputOptions, inputOptionToString


def displayNonDriveOptions():
    print(inputOptionToString(InputOptions.PARK))
    print(inputOptionToString(InputOptions.REVERSE))
    print(inputOptionToString(InputOptions.NEUTRAL))


startingRevs = 1500
revIncrement = 500


class Automatic(Automobile):

    def __init__(self, name, noGears, redLineRevs):
        self._currRevs = startingRevs
        self._redLineRevs = redLineRevs
        super().__init__(name, noGears)

    def _setPark(self):
        self.currGear = Gear.PARK

    def displayAccelData(self):
        print(f"Current RPMs  : {self._currRevs}")
        print(f"Current Speed : {int(self.currSpeed)}")
        time.sleep(0.1)

    def _accelerate(self, targetSpeed):
        print("\n===== Accelerating =====")
        while self.currSpeed < targetSpeed:
            print(f"\nCurrent Gear  : {self.currGear.name}")
            while self.currSpeed < targetSpeed and self._currRevs < self._redLineRevs:
                self._currRevs += revIncrement
                self.currSpeed = min(self.currSpeed + getAcceleration(self.currGear), targetSpeed)
                self.displayAccelData()
            if self.currSpeed != targetSpeed:
                try:
                    self._upShift()
                    self._currRevs = startingRevs
                except Exception as e:
                    print(f"{e}, cannot accelerate anymore")
                    print("\n===== Finished Accelerating =====")
                    return
        print("\n===== Finished Accelerating =====")

    def _decelerate(self, targetSpeed=0):
        print("\n===== Decelerating =====")
        while self.currSpeed > targetSpeed:
            print(f"\nCurrent Gear  : {self.currGear.name}")
            while self.currSpeed > targetSpeed and self._currRevs > startingRevs:
                self._currRevs -= revIncrement
                self.currSpeed = max(self.currSpeed - getAcceleration(self.currGear), targetSpeed)
                self.displayAccelData()
            if self.currSpeed != targetSpeed:
                try:
                    self._downShift()
                    self._currRevs = self._redLineRevs
                except Exception as e:
                    print(e)
                    print("\n===== Finished Decelerating =====")
                    return
        print("\n===== Finished Decelerating =====")

    def _displayOptions(self, inDrive):
        if inDrive:
            print(f"\nCurrent speed : {int(self.currSpeed)} mph\n")
            if self.currSpeed == 0:
                displayNonDriveOptions()
                print("\nChoose a gear to switch to (above) or enter a speed to accelerate to : ", end='')
            else:
                print("What speed would you like to go? : ", end='')
        else:
            print(f"\nCurrent Gear : {self.currGear.name}\n")
            displayNonDriveOptions()
            print(inputOptionToString(InputOptions.DRIVE))
            print(inputOptionToString(InputOptions.QUIT))
            print(f"\nWhat Gear would you like to switch too? (Options Above) : ", end='')

    def _drive(self):
        self._setNeutral()
        self._upShift()
        self._currRevs = startingRevs
        validInputs = [*InputOptions.PARK.value, *InputOptions.NEUTRAL.value, *InputOptions.REVERSE.value]
        while True:
            self._displayOptions(True)
            inputSpeed = input()
            if not inputSpeed.isnumeric():
                if inputSpeed in validInputs:
                    if self.currSpeed > 0:
                        print("\nYou must be stopped to change gears")
                        continue
                    else:
                        return inputSpeed
                else:
                    print("\nInvalid input")
                    continue
            targetSpeed = int(inputSpeed)
            if targetSpeed < 0:
                print("Speed must be greater than or equal to 0")
            elif targetSpeed < self.currSpeed:
                self._decelerate(targetSpeed)
            else:
                self._accelerate(targetSpeed)

    def _handleShiftChange(self, action):
        if action in InputOptions.PARK.value:
            self._setPark()
            return None
        elif action in InputOptions.REVERSE.value:
            self._setReverse()
            return None
        elif action in InputOptions.NEUTRAL.value:
            self._setNeutral()
            return None
        elif action in InputOptions.DRIVE.value:
            return self._drive()
        else:
            print("\nInvalid Input")

    def operate(self):
        action = InputOptions.PARK.value[0]
        while action not in InputOptions.QUIT.value:
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
