
import unittest
from unittest.mock import patch, Mock
from datetime import date, timedelta
from your_module import calculate_repayment_schedule

class TestCalculateRepaymentSchedule(unittest.TestCase):

    @patch('your_module.engine.connect')
    @patch('your_module.text')
    @patch('your_module.pd.Timedelta')
    def test_calculate_repayment_schedule(self, mock_pandas_timedelta, mock_text, mock_connect):
        # Mock the database connection
        conn = Mock()
        mock_connect.return_value = conn

        # Mock the query execution
        query = Mock()
        mock_text.return_value = query

        # Mock the fetchone method
        result = Mock()
        result.fetchone.return_value = (1000, 5, 60, date(2022, 1, 1))
        query.execute.return_value = result

        # Mock the pandas datetime.timedelta
        mock_pandas_timedelta.return_value = timedelta(days=30)

        # Call the function
        result = calculate_repayment_schedule(1)

        # Verify that the function was called correctly
        self.assertEqual(result, 0)
        mock_text.assert_called_once()
        query.execute.assert_called_once()
        conn.commit.assert_called_once()

    @patch('your_module.engine.connect')
    @patch('your_module.text')
    @patch('your_module.pd.Timedelta')
    def test_calculate_repayment_schedule_no_loan_found(self, mock_pandas_timedelta, mock_text, mock_connect):
        # Mock the database connection
        conn = Mock()
        mock_connect.return_value = conn

        # Mock the query execution
        query = Mock()
        mock_text.return_value = query

        # Mock the fetchone method
        result = None
        query.execute.return_value = result
        conn.execute.side_effect = Exception()

        # Mock the pandas datetime.timedelta
        mock_pandas_timedelta.return_value = timedelta(days=30)

        # Call the function
        self.assertRaises(Exception, calculate_repayment_schedule, 1)

    @patch('your_module.engine.connect')
    @patch('your_module.text')
    @patch('your_module.pd.Timedelta')
    def test_calculate_repayment_schedule_invalid_loan_id(self, mock_pandas_timedelta, mock_text, mock_connect):
        # Mock the database connection
        conn = Mock()
        mock_connect.return_value = conn

        # Mock the query execution
        query = Mock()
        mock_text.return_value = query

        # Mock the fetchone method
        result = None
        query.execute.return_value = result

        # Mock the pandas datetime.timedelta
        mock_pandas_timedelta.return_value = timedelta(days=30)

        # Call the function
        self.assertRaises(Exception, calculate_repayment_schedule, 0)

    @patch('your_module.engine.connect')
    @patch('your_module.text')
    @patch('your_module.pd.Timedelta')
    def test_calculate_repayment_schedule_invalid_loan_details(self, mock_pandas_timedelta, mock_text, mock_connect):
        # Mock the database connection
        conn = Mock()
        mock_connect.return_value = conn

        # Mock the query execution
        query = Mock()
        mock_text.return_value = query

        # Mock the fetchone method
        result = Mock()
        result.fetchone.return_value = (0, 1, 1, date(2022, 1, 1))
        query.execute.return_value = result

        # Mock the pandas datetime.timedelta
        mock_pandas_timedelta.return_value = timedelta(days=30)

        # Call the function
        self.assertRaises(Exception, calculate_repayment_schedule, 1)

if __name__ == '__main__':
    unittest.main()
