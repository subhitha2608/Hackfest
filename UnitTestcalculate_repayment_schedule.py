Python
import unittest
import pandas as pd
from unittest.mock import patch
from your_module import calculate_repayment_schedule

class TestCalculateRepaymentSchedule(unittest.TestCase):

    @patch('your_module.engine.connect')
    def test_calculate_repayment_schedule(self, mock_connect):
        # Mock the database connection
        conn = mock_connect.return_value
        conn.execute.return_value = [('1000', '5', '360', '2020-01-01')]

        # Test the function
        repayment_schedule = calculate_repayment_schedule(1)
        self.assertEqual(len(repayment_schedule), 12)
        self.assertEqual(repayment_schedule[0]['payment_date'], '2020-01-01')
        self.assertEqual(repayment_schedule[0]['total_payment'], 27.22401165151576)
        self.assertEqual(repayment_schedule[-1]['balance'], 0)

        # Test the function with a shorter loan term
        repayment_schedule = calculate_repayment_schedule(1)
        self.assertEqual(len(repayment_schedule), 6)
        self.assertEqual(repayment_schedule[0]['payment_date'], '2020-01-01')
        self.assertEqual(repayment_schedule[0]['total_payment'], 27.22401165151576)
        self.assertEqual(repayment_schedule[-1]['balance'], 0)

    @patch('your_module.engine.connect')
    def test_calculate_repayment_schedule_no_results(self, mock_connect):
        # Mock the database connection
        conn = mock_connect.return_value
        conn.execute.return_value = []

        # Test the function
        repayment_schedule = calculate_repayment_schedule(1)
        self.assertEqual(repayment_schedule, [])

    @patch('your_module.engine.connect')
    def test_calculate_repayment_schedule_error(self, mock_connect):
        # Mock the database connection
        conn = mock_connect.return_value
        conn.execute.side_effect = Exception('Invalid query')

        # Test the function
        with self.assertRaises(Exception):
            calculate_repayment_schedule(1)

if __name__ == '__main__':
    unittest.main()
