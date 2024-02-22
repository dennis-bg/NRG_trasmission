from NRG_trasmission.automobiles.Automobile import Automobile
from NRG_trasmission.automobiles.enums.Gear import Gear, gearToString
from NRG_trasmission.automobiles.enums.InputOptions import InputOptions, inputOptionToString


# Concrete class that describes Manual automobiles
# Extends Automobile class
class Manual(Automobile):

    def __init__(self, name, noGears):
        super().__init__(name, noGears)

    def _setGear(self, gear):
        if gear.value < Gear.FIRST.value:
            print("\nYou can not shift to a gear below First")
        elif gear.value > self.noGears:
            print(f"\nYour automobile only has {self.noGears} gears")
        else:
            self.currGear = gear

    # handles the user input to shift to the appropriate gear
    def _handleShiftChange(self, action):
        if action in InputOptions.DOWNSHIFT.value:
            try:
                self._downShift()
            except Exception as e:
                print(f"\n{e}")
        elif action in InputOptions.UPSHIFT.value:
            try:
                self._upShift()
            except Exception as e:
                print(f"\n{e}")
        elif action in InputOptions.NEUTRAL.value:
            self._setNeutral()
        elif self.currGear == Gear.NEUTRAL and action in InputOptions.REVERSE.value:
            self._setReverse()
        else:
            if not action.isnumeric():
                print("\nInvalid input")
                return
            gear = int(action)
            self._setGear(Gear(gear))

    # displays input options
    # shows options to UPSHIFT, DOWNSHIFT, NEUTRAL
    # shows numbered gears except the current numbered gear
    # if in NEUTRAL, shows REVERSE and QUIT
    def _displayOptions(self, inDrive):
        print(f"\nCurrent Gear : {self.currGear.name}\n")
        print("DOWNSHIFT : 'd' or 'D'")
        print(inputOptionToString(InputOptions.UPSHIFT))
        if self.currGear == Gear.NEUTRAL:
            print(inputOptionToString(InputOptions.REVERSE))
        print(inputOptionToString(InputOptions.NEUTRAL))
        for i in range(self.noGears):
            gear = Gear(i + 1)
            if self.currGear != gear:
                print(gearToString(gear))
        if self.currGear == Gear.NEUTRAL:
            print(inputOptionToString(InputOptions.QUIT))
        print(f"\nWhat Gear would you like to switch too? (Options Above) : ", end='')

    # controls user flow until they QUIT the automobile
    def operate(self):
        action = InputOptions.NEUTRAL.value[0]
        while action not in InputOptions.QUIT.value:
            self._handleShiftChange(action)
            self._displayOptions(False)
            nextAction = input()
            if self.currGear != Gear.NEUTRAL and nextAction in InputOptions.QUIT.value:
                print(f"\nYou must be in {Gear.NEUTRAL.name} to Quit")
            else:
                action = nextAction
