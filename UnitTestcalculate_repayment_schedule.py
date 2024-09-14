
import unittest
from unittest.mock import patch
from your_module import calculate_repayment_schedule  # replace 'your_module' with the actual name of your module

class TestCalculateRepaymentSchedule(unittest.TestCase):

    @patch('config.engine')
    @patch('sqlalchemy.text')
    @patch('pandas.Timedelta')
    def test_calculate_repayment_schedule(self, mock_Timedelta, mock_text, mock_engine):
        # Test 1: Successful execution of the function
        mock_result = [(1000, 4.5, 6, '2022-01-01')]
        mock_engine.return_value.execute.return_value.fetchall.return_value = [mock_result]
        with patch.object(mock_engine.return_value, 'begin', return_value=mock_engine.return_value) as mock_conn:
            self.assertTrue(calculate_repayment_schedule(1))
            mock_conn.commit.assert_called_once()

        # Test 2: Fail to execute the function
        mock_engine.return_value.execute.return_value.fetchall.return_value = None
        with self.assertRaises(Exception):
            calculate_repayment_schedule(1)
            mock_engine.return_value.execute.return_value.execute.assert_not_called()

        # Test 3: Invalid loan id
        with self.assertRaises(Exception):
            calculate_repayment_schedule(0)
            mock_engine.return_value.execute.return_value.execute.assert_not_called()

        # Test 4: Invalid loan term
        mock_result = [(1000, 4.5, 'abc', '2022-01-01')]
        mock_engine.return_value.execute.return_value.fetchall.return_value = [mock_result]
        with self.assertRaises(Exception):
            calculate_repayment_schedule(1)
            mock_engine.return_value.execute.return_value.execute.assert_not_called()

if __name__ == '__main__':
    unittest.main()
