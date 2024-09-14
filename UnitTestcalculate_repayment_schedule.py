
import unittest
from unittest.mock import patch, Mock
from sqlalchemy import text
import pandas as pd
import psycopg2

class TestCalculateRepaymentSchedule(unittest.TestCase):

    @patch('config.engine')
    def test_calculate_repayment_schedule_found(self, mock_engine):
        mock_conn = Mock()
        mock_engine.connect.return_value = mock_conn
        mock_result = Mock()
        mock_conn.execute.return_value = mock_result
        mock_result.fetchone.return_value = (1000, 5, 60, pd.to_datetime('2022-01-01'))

        repayment_schedule = calculate_repayment_schedule(1)
        self.assertEqual(len(repayment_schedule), 60)

    @patch('config.engine')
    def test_calculate_repayment_schedule_not_found(self, mock_engine):
        mock_conn = Mock()
        mock_engine.connect.return_value = mock_conn
        mock_result = Mock()
        mock_conn.execute.return_value = mock_result
        mock_result.fetchone.return_value = None

        with self.assertRaises(ValueError):
            calculate_repayment_schedule(1)

    @patch('config.engine')
    def test_calculate_repayment_schedule_insertion(self, mock_engine):
        mock_conn = Mock()
        mock_engine.connect.return_value = mock_conn
        mock_result = Mock()
        mock_conn.execute.return_value = mock_result
        mock_result.fetchone.return_value = (1000, 5, 60, pd.to_datetime('2022-01-01'))

        with patch.object(mock_conn, 'execute') as mock_execute:
            calculate_repayment_schedule(1)
            self.assertEqual(mock_execute.call_count, 61)

    @patch('config.engine')
    def test_calculate_repayment_schedule_commit(self, mock_engine):
        mock_conn = Mock()
        mock_engine.connect.return_value = mock_conn
        mock_result = Mock()
        mock_conn.execute.return_value = mock_result
        mock_result.fetchone.return_value = (1000, 5, 60, pd.to_datetime('2022-01-01'))

        with patch.object(mock_conn, 'commit') as mock_commit:
            calculate_repayment_schedule(1)
            self.assertEqual(mock_commit.call_count, 1)

if __name__ == '__main__':
    unittest.main()
