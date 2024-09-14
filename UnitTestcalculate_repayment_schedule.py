
import unittest
from unittest.mock import patch, Mock
from sqlalchemy import create_engine, text
import pandas as pd
import psycopg2
from your_module import calculate_repayment_schedule

class TestCalculateRepaymentSchedule(unittest.TestCase):
    @patch('your_module.engine')
    def test_calculate_repayment_schedule(self, mock_engine):
        # Setup mock engine connection
        mock_conn = Mock()
        mock_engine.connect.return_value = mock_conn

        # Setup mock query result
        mock_result = Mock()
        mock_result.fetchone.return_value = (1000, 5, 12, '2022-01-01')
        mock_conn.execute.return_value = mock_result

        # Test loan exists
        loan_id = 1
        repayment_schedule = calculate_repayment_schedule(loan_id)
        self.assertIsInstance(repayment_schedule, pd.DataFrame)

        # Test loan does not exist
        mock_result.fetchone.return_value = None
        with self.assertRaises(ValueError):
            calculate_repayment_schedule(loan_id)

        # Test loan term is 0
        mock_result.fetchone.return_value = (1000, 5, 0, '2022-01-01')
        with self.assertRaises(ValueError):
            calculate_repayment_schedule(loan_id)

        # Test loan amount is 0
        mock_result.fetchone.return_value = (0, 5, 12, '2022-01-01')
        with self.assertRaises(ValueError):
            calculate_repayment_schedule(loan_id)

        # Test interest rate is 0
        mock_result.fetchone.return_value = (1000, 0, 12, '2022-01-01')
        with self.assertRaises(ValueError):
            calculate_repayment_schedule(loan_id)

        # Test start date is None
        mock_result.fetchone.return_value = (1000, 5, 12, None)
        with self.assertRaises(ValueError):
            calculate_repayment_schedule(loan_id)

if __name__ == '__main__':
    unittest.main()
