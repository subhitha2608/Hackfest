
import unittest
from unittest.mock import patch, Mock
from calculate_repayment_schedule import calculate_repayment_schedule

class TestCalculateRepaymentSchedule(unittest.TestCase):

    @patch('config.engine.connect')
    @patch('config.engine.execute')
    def test_calculate_repayment_schedule(self, mock_execute, mock_connect):
        # Arrange
        conn = mock_connect.return_value
        result1 = pd.DataFrame({'loanamount': [1000], 'interestrate': [5], 'loanterm': [12], 'startdate': ['2022-01-01']})
        conn.execute.return_value = result1
        result2 = pd.DataFrame({'balance': [0]})
        mock_execute.return_value = result2

        # Act
        result = calculate_repayment_schedule(1)

        # Assert
        self.assertEqual(result, 0.0)

    @patch('config.engine.connect')
    @patch('config.engine.execute')
    def test_calculate_repayment_schedule_invalid_loanid(self, mock_execute, mock_connect):
        # Arrange
        conn = mock_connect.return_value
        mock_execute.side_effect = psycopg2.Error('Invalid loan ID')

        # Act and Assert
        with self.assertRaises(Exception):
            calculate_repayment_schedule(1)

    @patch('config.engine.connect')
    @patch('config.engine.execute')
    def test_calculate_repayment_schedule_database_error(self, mock_execute, mock_connect):
        # Arrange
        conn = mock_connect.return_value
        mock_execute.side_effect = psycopg2.Error('Database error')

        # Act and Assert
        with self.assertRaises(Exception):
            calculate_repayment_schedule(1)

    @patch('config.engine.connect')
    @patch('config.engine.execute')
    def test_calculate_repayment_schedule_connection_error(self, mock_execute, mock_connect):
        # Arrange
        mock_connect.side_effect = psycopg2.OperationalError('Connection error')

        # Act and Assert
        with self.assertRaises(Exception):
            calculate_repayment_schedule(1)

if __name__ == '__main__':
    unittest.main()
