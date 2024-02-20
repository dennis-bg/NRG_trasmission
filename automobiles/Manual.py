from NRG_trasmission.automobiles.Automobile import Automobile
from NRG_trasmission.automobiles.Gear import Gear


class Manual(Automobile):

    def __init__(self, name, noGears):
        super().__init__(name, noGears)

    def __setGear(self, gear):
        if gear.value < 1:
            print("\nYou can not shift to a gear below First")
        elif gear.value > self.noGears:
            print(f"\nYour automobile only has {self.noGears} gears")
        else:
            self.currGear = gear

    def _handleShiftChange(self, action):
        if action in ['d', 'D']:
            try:
                self._downShift()
            except Exception as e:
                print(f"\n{e}")
        elif action in ['u', 'U']:
            try:
                self._upShift()
            except Exception as e:
                print(f"\n{e}")
        elif action in ['n', 'N']:
            self._setNeutral()
        elif action in ['r', 'R']:
            self._setReverse()
        else:
            if not action.isnumeric():
                print("\nNot a valid input")
                return
            gear = int(action)
            self.__setGear(Gear(gear))

    def _displayOptions(self, inDrive):
        print(f"\nCurrent Gear : {self.currGear.name}\n")
        print(f"Down Shift 1 gear : 'd' or 'D'\nUp Shift 1 gear : 'u' or 'U'")
        print(f"{Gear.REVERSE.name} : 'r' or 'R'\n{Gear.NEUTRAL.name} : 'n' or 'N'")
        for i in range(self.noGears):
            print(f"{Gear(i + 1).name} : '{Gear(i + 1).value}'")
        print(f"QUIT {self.name} : 'q' or 'Q'")
        print(f"\nWhat Gear would you like to switch too? (Options Above) : ", end='')

    def operate(self):
        action = 'n'
        while action not in ['q', 'Q']:
            self._handleShiftChange(action)
            self._displayOptions(False)
            action = input()


def main():
    manual_car = Manual("Toyota", 5)
    manual_car.operate()


if __name__ == "__main__":
    main()
