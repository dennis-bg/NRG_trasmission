import unittest
from io import StringIO

from unittest.mock import patch

from NRG_trasmission.automobiles.Automatic import Automatic, displayNonDriveOptions
from NRG_trasmission.automobiles.enums.Gear import Gear


class TestAutomatic(unittest.TestCase):

    def setUp(self):
        self.automatic_car = Automatic("Test Car", 6, 6000)

    def test_initialization(self):
        self.assertEqual(self.automatic_car.name, "Test Car")
        self.assertEqual(self.automatic_car.noGears, 6)
        self.assertEqual(self.automatic_car.currGear, Gear.NEUTRAL)
        self.assertEqual(self.automatic_car.currSpeed, 0)
        self.assertEqual(self.automatic_car._currRevs, 1500)
        self.assertEqual(self.automatic_car._redLineRevs, 6000)

    def test_setPark(self):
        self.automatic_car.currGear = Gear.NEUTRAL
        self.assertNotEqual(self.automatic_car.currGear, Gear.PARK)
        self.automatic_car._setPark()
        self.assertEqual(self.automatic_car.currGear, Gear.PARK)

    def test_accelerate(self):
        self.automatic_car.currGear = Gear.FIRST
        self.automatic_car._accelerate(20)
        self.assertEqual(self.automatic_car.currSpeed, 20)
        self.automatic_car._accelerate(10)
        self.assertEqual(self.automatic_car.currSpeed, 20)

    def test_decelerate(self):
        self.automatic_car.currGear = Gear.SECOND
        self.automatic_car._currRevs = 2500
        self.automatic_car.currSpeed = 20
        self.automatic_car._decelerate(0)
        self.assertEqual(self.automatic_car.currSpeed, 0)
        self.automatic_car._decelerate(10)
        self.assertEqual(self.automatic_car.currSpeed, 0)

    @patch('NRG_trasmission.automobiles.Automatic.Automatic._setPark')
    def test_handleShiftChange_park(self, mock_park):
        shiftChangeReturnVal = self.automatic_car._handleShiftChange('p')
        self.assertEqual(mock_park.call_count, 1)
        self.assertEqual(shiftChangeReturnVal, None)
        shiftChangeReturnVal = self.automatic_car._handleShiftChange('P')
        self.assertEqual(mock_park.call_count, 2)
        self.assertEqual(shiftChangeReturnVal, None)

    @patch('NRG_trasmission.automobiles.Automatic.Automatic._setNeutral')
    def test_handleShiftChange_neutral(self, mock_neutral):
        shiftChangeReturnVal = self.automatic_car._handleShiftChange('n')
        self.assertEqual(mock_neutral.call_count, 1)
        self.assertEqual(shiftChangeReturnVal, None)
        shiftChangeReturnVal = self.automatic_car._handleShiftChange('N')
        self.assertEqual(mock_neutral.call_count, 2)
        self.assertEqual(shiftChangeReturnVal, None)

    @patch('NRG_trasmission.automobiles.Automatic.Automatic._setReverse')
    def test_handleShiftChange_reverse(self, mock_reverse):
        shiftChangeReturnVal = self.automatic_car._handleShiftChange('r')
        self.assertEqual(mock_reverse.call_count, 1)
        self.assertEqual(shiftChangeReturnVal, None)
        shiftChangeReturnVal = self.automatic_car._handleShiftChange('R')
        self.assertEqual(mock_reverse.call_count, 2)
        self.assertEqual(shiftChangeReturnVal, None)

    @patch('NRG_trasmission.automobiles.Automatic.Automatic._drive')
    def test_handleShiftChange_drive(self, mock_drive):
        mock_drive.return_value = 'p'
        shiftChangeReturnVal = self.automatic_car._handleShiftChange('d')
        self.assertEqual(mock_drive.call_count, 1)
        self.assertEqual(shiftChangeReturnVal, 'p')
        mock_drive.return_value = 'N'
        shiftChangeReturnVal = self.automatic_car._handleShiftChange('D')
        self.assertEqual(mock_drive.call_count, 2)
        self.assertEqual(shiftChangeReturnVal, 'N')

    # @patch('builtins.input', side_effect=['5', '15', 'p'])
    # @patch('NRG_trasmission.automobiles.Automatic.Automatic._accelerate')
    # @patch('NRG_trasmission.automobiles.Automatic.Automatic._decelerate')
    # def test_drive(self, mock_decelerate, mock_accelerate, mock_input):
    #     self.automatic_car.currSpeed = 10
    #     returnVal = self.automatic_car._drive()
    #     mock_decelerate.assert_called_once_with(5)
    #     mock_accelerate.assert_called_once_with(15)
    #     self.assertEqual(returnVal, 'p')

    @patch('builtins.input', side_effect=['n', 'r', 'p', 'q', 'd', 'q'])
    @patch('NRG_trasmission.automobiles.Automatic.Automatic._handleShiftChange')
    @patch('NRG_trasmission.automobiles.Automatic.Automatic._displayOptions')
    def test_operate_not_drive(self, mock_displayOptions, mock_handleShiftChange, mock_input):
        mock_handleShiftChange.return_value = None
        self.automatic_car.operate()
        self.assertEqual(mock_handleShiftChange.call_count, 4)
        self.assertEqual(mock_displayOptions.call_count, 4)
        mock_handleShiftChange.return_value = 'P'
        self.automatic_car.operate()
        self.assertEqual(mock_handleShiftChange.call_count, 8)
        self.assertEqual(mock_displayOptions.call_count, 6)

    @patch('sys.stdout', new_callable=StringIO)
    def test_displayNonDriveOptions(self, mock_stdout):
        expected_output = f"{Gear.PARK.name}      : 'p' or 'P'\n" \
                          f"{Gear.REVERSE.name}   : 'r' or 'R'\n" \
                          f"{Gear.NEUTRAL.name}   : 'n' or 'N'\n"
        displayNonDriveOptions()
        self.assertEqual(mock_stdout.getvalue(), expected_output)

    @patch('sys.stdout', new_callable=StringIO)
    def test_displayOptions_in_drive_stopped(self, mock_stdout):
        self.automatic_car._displayOptions(True)
        expected_output = "\nCurrent speed : 0 mph\n" \
                          f"\n{Gear.PARK.name}      : 'p' or 'P'\n" \
                          f"{Gear.REVERSE.name}   : 'r' or 'R'\n" \
                          f"{Gear.NEUTRAL.name}   : 'n' or 'N'\n" \
                          "\nChoose a gear to switch to (above) or enter a speed to accelerate to : "
        self.assertEqual(mock_stdout.getvalue(), expected_output)

    @patch('sys.stdout', new_callable=StringIO)
    def test_displayOptions_in_drive_moving(self, mock_stdout):
        self.automatic_car.currSpeed = 10
        self.automatic_car._displayOptions(True)
        expected_output = "\nCurrent speed : 10 mph\n" \
                          "\nWhat speed would you like to go? : "
        self.assertEqual(mock_stdout.getvalue(), expected_output)


if __name__ == '__main__':
    unittest.main()
