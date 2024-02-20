import unittest
from unittest.mock import patch
from io import StringIO
from NRG_trasmission.automobiles.Automatic import Automatic, displayNonDriveOptions, Gear


class TestAutomatic(unittest.TestCase):

    def setUp(self):
        self.automatic_car = Automatic("Toyota", 5, 6000)

    def test_accelerate(self):
        self.automatic_car.currGear = Gear.FIRST
        self.automatic_car.accelerate(20)
        self.assertEqual(self.automatic_car.currSpeed, 20)

    def test_decelerate(self):
        self.automatic_car.currSpeed = 20
        self.automatic_car.currGear = Gear.FIRST
        self.automatic_car.decelerate(10)
        self.assertEqual(self.automatic_car.currSpeed, 10)

    def test_display_options(self):
        captured_output = StringIO()
        expected_output = f"\nCurrent Gear : {self.automatic_car.currGear.name}\n" \
                          f"{Gear.PARK.name}    : 'p' or 'P'\n" \
                          f"{Gear.REVERSE.name} : 'r' or 'R'\n" \
                          f"{Gear.NEUTRAL.name} : 'n' or 'N'\n" \
                          f"DRIVE   : 'd' or 'D'\n" \
                          f"QUIT {self.automatic_car.name} : 'q' or 'Q'\n" \
                          f"\nWhat Gear would you like to switch too? (Options Above) : "

        with patch('sys.stdout', new=captured_output):
            self.automatic_car.displayOptions(False)
            self.assertEqual(captured_output.getvalue(), expected_output)

    def test_set_park(self):
        self.automatic_car.currGear = Gear.FIRST
        self.automatic_car.setPark()
        self.assertEqual(self.automatic_car.currGear, Gear.PARK)

    @patch('builtins.input', side_effect=['20'])
    def test_drive(self, mock_input):
        with patch('sys.stdout', new=StringIO()) as fake_out:
            self.automatic_car.drive()
            self.assertEqual(fake_out.getvalue().strip(), 'What speed would you like to go? :')

    def test_handle_shift_change(self):
        self.automatic_car.handleShiftChange('p')
        self.assertEqual(self.automatic_car.currGear, Gear.PARK)

    def test_operate(self):
        with patch('builtins.input', side_effect=['q']):
            with patch('sys.stdout', new=StringIO()) as fake_out:
                self.automatic_car.operate()
                self.assertIn('What Gear would you like to switch too?', fake_out.getvalue())


if __name__ == '__main__':
    unittest.main()
