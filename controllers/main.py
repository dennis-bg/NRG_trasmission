from NRG_trasmission.automobiles.Automatic import Automatic
from NRG_trasmission.automobiles.Manual import Manual


def getNoGears(name):
    noGears = "!"
    while not noGears.isnumeric() or int(noGears) > 10 or int(noGears) < 1:
        print(f"\nHow many gears does your {name} have? (Number between 1 and 10) : ", end='')
        noGears = input()
    return int(noGears)


def getTransmission(name):
    isManual = "!"
    while isManual not in ['m', 'M', 'a', 'A']:
        print("\nAutomatic : 'a' or 'A'")
        print("Manual    : 'm' or 'M'")
        print(f"\nDoes your {name} have a manual or automatic transmission ? (Options Above) : ", end='')
        isManual = input()
    return isManual in ['m', 'M']


def getRedLine():
    redLine = "!"
    while not redLine.isnumeric():
        print("\nAt what RPM does the engine start to red line? : ", end='')
        redLine = input()
    return int(redLine)


def getName():
    print("\nName of your car ('q' or 'Q' to quit application) : ", end='')
    name = input()
    return name


def main():
    while True:
        name = getName()
        if name in ['q', 'Q']:
            break
        noGears = getNoGears(name)
        isManual = getTransmission(name)
        redLine = 0 if isManual else getRedLine()
        automobile = Manual(name, noGears) if isManual else Automatic(name, noGears, redLine)
        automobile.operate()
        print("\n========================================================\n")


if __name__ == '__main__':
    main()
