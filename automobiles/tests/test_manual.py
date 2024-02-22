import unittest
from unittest.mock import patch
from io import StringIO

from NRG_trasmission.automobiles.enums.Gear import Gear
from NRG_trasmission.automobiles.Manual import Manual


class TestManual(unittest.TestCase):

    def setUp(self):
        self.manual_car = Manual("Test Car", 5)

    def test_initialization(self):
        self.assertEqual(self.manual_car.name, "Test Car")
        self.assertEqual(self.manual_car.noGears, 5)
        self.assertEqual(self.manual_car.currGear, Gear.NEUTRAL)
        self.assertEqual(self.manual_car.currSpeed, 0)

    @patch('NRG_trasmission.automobiles.Manual.Manual._upShift')
    def test_handleShiftChange_up(self, mock_upshift):
        self.manual_car.currGear = Gear.FIRST
        self.manual_car._handleShiftChange('u')
        self.assertEqual(mock_upshift.call_count, 1)
        self.manual_car._handleShiftChange('U')
        self.assertEqual(mock_upshift.call_count, 2)

    @patch('NRG_trasmission.automobiles.Manual.Manual._downShift')
    def test_handleShiftChange_down(self, mock_downshift):
        self.manual_car.currGear = Gear.THIRD
        self.manual_car._handleShiftChange('d')
        self.assertEqual(mock_downshift.call_count, 1)
        self.manual_car._handleShiftChange('D')
        self.assertEqual(mock_downshift.call_count, 2)

    @patch('NRG_trasmission.automobiles.Manual.Manual._setNeutral')
    def test_handleShiftChange_neutral(self, mock_neutral):
        self.manual_car._handleShiftChange('n')
        self.assertEqual(mock_neutral.call_count, 1)
        self.manual_car._handleShiftChange('N')
        self.assertEqual(mock_neutral.call_count, 2)

    @patch('NRG_trasmission.automobiles.Manual.Manual._setReverse')
    def test_handleShiftChange_reverse(self, mock_reverse):
        self.manual_car._handleShiftChange('r')
        self.assertEqual(mock_reverse.call_count, 1)
        self.manual_car._handleShiftChange('R')
        self.assertEqual(mock_reverse.call_count, 2)

    @patch('sys.stdout', new_callable=StringIO)
    def test_handleShiftChange_invalid(self, mock_stdout):
        expected_output = "\nNot a valid input\n"
        self.manual_car._handleShiftChange('a')
        self.assertEqual(mock_stdout.getvalue(), expected_output)

    @patch('NRG_trasmission.automobiles.Manual.Manual._setGear')
    def test_handleShiftChange_setGear(self, mock_setGear):
        self.manual_car._handleShiftChange('1')
        mock_setGear.assert_called_once_with(Gear.FIRST)
        self.manual_car._handleShiftChange('2')
        mock_setGear.assert_called_with(Gear.SECOND)
        self.manual_car._handleShiftChange('3')
        mock_setGear.assert_called_with(Gear.THIRD)
        self.manual_car._handleShiftChange('4')
        mock_setGear.assert_called_with(Gear.FOURTH)
        self.manual_car._handleShiftChange('5')
        mock_setGear.assert_called_with(Gear.FIFTH)

    @patch('sys.stdout', new_callable=StringIO)
    def test_displayOptions(self, mock_stdout):
        self.manual_car._displayOptions(False)
        expected_output = "\nCurrent Gear : NEUTRAL\n" \
                          "\nDOWNSHIFT : 'd' or 'D'\n" \
                          "UPSHIFT   : 'u' or 'U'\n" \
                          "REVERSE   : 'r' or 'R'\n" \
                          "NEUTRAL   : 'n' or 'N'\n" \
                          "FIRST     : '1'\n" \
                          "SECOND    : '2'\n" \
                          "THIRD     : '3'\n" \
                          "FOURTH    : '4'\n" \
                          "FIFTH     : '5'\n" \
                          "QUIT      : 'q' or 'Q'\n" \
                          "\nWhat Gear would you like to switch too? (Options Above) : "
        self.assertEqual(mock_stdout.getvalue(), expected_output)

    @patch('builtins.input', side_effect=['1', '2', '3', 'n', 'r', 'n', 'q'])
    @patch('NRG_trasmission.automobiles.Manual.Manual._handleShiftChange')
    @patch('NRG_trasmission.automobiles.Manual.Manual._displayOptions')
    def test_operate(self, mock_displayOptions, mock_handleShiftChange, mock_input):
        self.manual_car.operate()
        self.assertEqual(mock_handleShiftChange.call_count, 7)
        self.assertEqual(mock_displayOptions.call_count, 7)


if __name__ == '__main__':
    unittest.main()
