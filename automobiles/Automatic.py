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


# Concrete class that describes Automatic automobiles
# Extends Automobile class
class Automatic(Automobile):

    def __init__(self, name, noGears, redLineRevs):
        self._currRevs = startingRevs
        self._redLineRevs = redLineRevs
        super().__init__(name, noGears)

    # puts the car in PARK for automatic automobiles
    def _setPark(self):
        self.currGear = Gear.PARK

    # displays the current RPMs and speed while accelerating and decelerating
    def displayAccelData(self):
        print(f"Current RPMs  : {self._currRevs}")
        print(f"Current Speed : {int(self.currSpeed)}")
        time.sleep(0.1)

    # accelerates from current speed to target speed
    # increases RPMs until redline and then upshifts if possible, repeats until currSpeed = targetSpeed
    def _accelerate(self, targetSpeed):
        print("\n===== Accelerating =====")
        # loop to shift gears up until target speed reached
        while self.currSpeed < targetSpeed:
            print(f"\nCurrent Gear  : {self.currGear.name}")
            # loop to increase RPMs until target speed reached
            while self.currSpeed < targetSpeed and self._currRevs < self._redLineRevs:
                self._currRevs += revIncrement
                self.currSpeed = min(self.currSpeed + getAcceleration(self.currGear), targetSpeed)
                self.displayAccelData()
            if self.currSpeed != targetSpeed:
                # upshift if possible
                try:
                    self._upShift()
                    self._currRevs = startingRevs
                except Exception as e:
                    print(f"{e}, cannot accelerate anymore")
                    print("\n===== Finished Accelerating =====")
                    return
        print("\n===== Finished Accelerating =====")

    # decelerates from current speed to target speed
    # decreases RPMs until startingRevs and then downshifts if possible, repeats until currSpeed = targetSpeed
    def _decelerate(self, targetSpeed=0):
        print("\n===== Decelerating =====")
        # loop to shift gears down until target speed reached
        while self.currSpeed > targetSpeed:
            print(f"\nCurrent Gear  : {self.currGear.name}")
            # loop to decrease RPMs until target speed reached
            while self.currSpeed > targetSpeed and self._currRevs > startingRevs:
                self._currRevs -= revIncrement
                self.currSpeed = max(self.currSpeed - getAcceleration(self.currGear), targetSpeed)
                self.displayAccelData()
            if self.currSpeed != targetSpeed:
                # downshift if possible
                try:
                    self._downShift()
                    self._currRevs = self._redLineRevs
                except Exception as e:
                    print(e)
                    print("\n===== Finished Decelerating =====")
                    return
        print("\n===== Finished Decelerating =====")

    # displays input options
    # if not in drive, option to PARK, REVERSE, NEUTRAL, and DRIVE
    # if in drive but not moving, option to PARK, REVERSE, NEUTRAL, or accelerate to a speed
    # if moving, only option to change speed
    # if in PARK, option to QUIT
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

    # controls user flow when automobile is put in DRIVE
    # if stopped, allows to change gears
    # otherwise allows user to choose a speed to accelerate or decelerate to
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

    # handles the user input to shift to the appropriate gear
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

    # controls user flow until they QUIT the automobile
    def operate(self):
        action = InputOptions.PARK.value[0]
        while action not in InputOptions.QUIT.value:
            shiftFromDrive = self._handleShiftChange(action)
            if shiftFromDrive is not None:
                self._handleShiftChange(shiftFromDrive)
            self._displayOptions(False)
            action = input()
