
import unittest
from unittest.mock import patch, Mock
from datetime import date
from your_module import calculate_repayment_schedule  # Replace 'your_module' with the actual module name

class TestCalculateRepaymentSchedule(unittest.TestCase):
    @patch('config.engine.connect')
    @patch('config.engine.fetchall')
    def test_calculate_repayment_schedule(self, mock_fetchall, mock_connect):
        # Setup mock data
        loan_id = 1
        loan_amount = 100000
        interest_rate = 5
        loan_term = 5
        start_date = date(2022, 1, 1)

        # Setup mock queries
        query_result = [(loan_amount, interest_rate / 100 / 12, loan_term, start_date)]
        mock_fetchall.return_value = query_result

        mock_query = Mock(return_value=Mock(return_value=query_result))
        mock_query.fetchone.return_value = query_result[0]

        # Call the function
        result = calculate_repayment_schedule(loan_id)

        # Assertions
        self.assertEqual(len(result), loan_term)
        self.assertEqual(result[0]['paymentnumber'], 1)
        self.assertEqual(result[0]['balance'], loan_amount)

        # Test edge cases
        self.assertRaises(IndexError, calculate_repayment_schedule, None)
        self.assertRaises(TypeError, calculate_repayment_schedule, 'abc')

if __name__ == '__main__':
    unittest.main()
