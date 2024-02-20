import unittest

from NRG_trasmission.automobiles.Gear import Gear
from NRG_trasmission.automobiles.Manual import Manual


class TestAutomobile(unittest.TestCase):

    def setUp(self):
        self.automobile = Manual("Test Car", 5)

    def test_initialization(self):
        self.assertEqual(self.automobile.name, "Test Car")
        self.assertEqual(self.automobile.noGears, 5)
        self.assertEqual(self.automobile.currGear, Gear.NEUTRAL)
        self.assertEqual(self.automobile.currSpeed, 0)

    def test_currSpeed_setter(self):
        self.automobile.currSpeed = 50
        self.assertEqual(self.automobile.currSpeed, 50)

    def test_currGear_setter(self):
        self.automobile.currGear = Gear.FIRST
        self.assertEqual(self.automobile.currGear, Gear.FIRST)

    def test_setNeutral(self):
        self.automobile.currGear = Gear.FIRST
        self.automobile._setNeutral()
        self.assertEqual(self.automobile.currGear, Gear.NEUTRAL)

    def test_setReverse(self):
        self.automobile._setReverse()
        self.assertEqual(self.automobile.currGear, Gear.REVERSE)

    def test_upShift(self):
        self.automobile.currGear = Gear.FIRST
        self.automobile._upShift()
        self.assertEqual(self.automobile.currGear, Gear.SECOND)

        self.automobile.currGear = self.automobile.noGears
        with self.assertRaises(Exception):
            self.automobile._upShift()

    def test_downShift(self):
        self.automobile.currGear = Gear.SECOND
        self.automobile._downShift()
        self.assertEqual(self.automobile.currGear, Gear.FIRST)

        self.automobile.currGear = Gear.NEUTRAL
        with self.assertRaises(Exception):
            self.automobile._downShift()

        self.automobile.currGear = Gear.REVERSE
        with self.assertRaises(Exception):
            self.automobile._downShift()


if __name__ == '__main__':
    unittest.main()
