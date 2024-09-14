
import unittest
from unittest.mock import patch, Mock
from your_module import calculate_repayment_schedule

class TestCalculateRepaymentSchedule(unittest.TestCase):
    @patch('your_module.engine')
    @patch('your_module.text')
    def test_calculate_repayment_schedule(self, mock_text, mock_engine):
        # Mock the database query to return a loan record with a valid loan id
        loan_id = 123
        result = {'loanamount': 10000, 'interestrate': 5, 'loanterm': 360, 'startdate': '2022-01-01'}
        mock_text.return_value = 'SELECT loanamount, interestrate, loanterm, startdate FROM loans WHERE loanid = :loan_id'
        mock_engine.execute.return_value = Mock(fetchone= lambda: result)

        # Call the function
        repayment_schedule = calculate_repayment_schedule(loan_id)

        # Verify the function execution
        mock_engine.execute.assert_called_once_with(mock_text.return_value, loan_id=loan_id)
        self.assertEqual(len(repayment_schedule), result['loanterm'])

        # Verify each payment in the schedule
        for payment in repayment_schedule:
            self.assertIn('paymentnumber', payment)
            self.assertIn('paymentdate', payment)
            self.assertIn('principalamount', payment)
            self.assertIn('interestamount', payment)
            self.assertIn('totalpayment', payment)
            self.assertIn('balance', payment)

    @patch('your_module.engine')
    @patch('your_module.text')
    def test_calculate_repayment_schedule_invalid_loan_id(self, mock_text, mock_engine):
        # Mock the database query to return a loan record with an invalid loan id
        loan_id = 99999
        mock_text.return_value = 'SELECT loanamount, interestrate, loanterm, startdate FROM loans WHERE loanid = :loan_id'
        mock_engine.execute.return_value = Mock(fetchone= lambda: None)

        # Call the function
        with self.assertRaises(ValueError):
            calculate_repayment_schedule(loan_id)

        # Verify the function execution
        mock_engine.execute.assert_called_once_with(mock_text.return_value, loan_id=loan_id)
        self.assertIsNone(repayment_schedule)

    @patch('your_module.engine')
    @patch('your_module.text')
    def test_calculate_repayment_schedule_zero_loan_term(self, mock_text, mock_engine):
        # Mock the database query to return a loan record with a zero loan term
        loan_id = 123
        result = {'loanamount': 10000, 'interestrate': 5, 'loanterm': 0, 'startdate': '2022-01-01'}
        mock_text.return_value = 'SELECT loanamount, interestrate, loanterm, startdate FROM loans WHERE loanid = :loan_id'
        mock_engine.execute.return_value = Mock(fetchone= lambda: result)

        # Call the function
        repayment_schedule = calculate_repayment_schedule(loan_id)

        # Verify the function execution
        mock_engine.execute.assert_called_once_with(mock_text.return_value, loan_id=loan_id)
        self.assertEqual(len(repayment_schedule), 0)

if __name__ == '__main__':
    unittest.main()
