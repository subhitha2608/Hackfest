
import unittest
from unittest.mock import patch, MagicMock
from datetime import date, timedelta
import pandas as pd

class TestGenerateRepaymentSchedule(unittest.TestCase):
    def setUp(self):
        self.loan_id = 1
        self.loan_amount = 10000
        self.interest_rate = 5
        self.loan_term = 12
        self.start_date = date(2022, 1, 1)

    @patch('config.engine')
    @patch('sqlalchemy.sql.expression.Text')
    def test_generate_repayment_schedule(self, mock_text, mock_engine):
        # Mock the loan details query result
        mock_result = MagicMock()
        mock_result.fetchone.return_value = (self.loan_amount, self.interest_rate, self.loan_term, self.start_date)
        mock_engine.connect.return_value.__enter__ = mock_result

        # Mock the execute method of the engine connection
        mock_execute = MagicMock()
        mock_execute.return_value = mock_result
        mock_engine.connect.return_value.__enter__.execute = mock_execute

        # Mock the commit method of the engine connection
        mock_commit = MagicMock()
        mock_engine.connect.return_value.__enter__.commit = mock_commit

        # Call the generate_repayment_schedule function
        repayment_schedule = generate_repayment_schedule(self.loan_id)

        # Assert the repayment schedule is a pandas DataFrame
        self.assertIsInstance(repayment_schedule, pd.DataFrame)

        # Assert the repayment schedule has the correct columns
        self.assertEqual(repayment_schedule.columns.tolist(), [
            'loanid', 'paymentnumber', 'paymentdate', 'principalamount', 'interestamount', 'totalpayment', 'balance'
        ])

        # Assert the repayment schedule has the correct number of rows
        self.assertEqual(len(repayment_schedule), self.loan_term)

        # Assert the loan details were extracted correctly
        self.assertEqual(repayment_schedule.iloc[0]['loanid'], self.loan_id)
        self.assertEqual(repayment_schedule.iloc[0]['principalamount'], self.loan_amount / self.loan_term)
        self.assertEqual(repayment_schedule.iloc[0]['interestamount'], self.loan_amount * self.interest_rate / 100 / 12)
        self.assertEqual(repayment_schedule.iloc[0]['totalpayment'], self.loan_amount / self.loan_term + self.loan_amount * self.interest_rate / 100 / 12)
        self.assertEqual(repayment_schedule.iloc[0]['balance'], self.loan_amount - self.loan_amount / self.loan_term)

    @patch('config.engine')
    @patch('sqlalchemy.sql.expression.Text')
    def test_generate_repayment_schedule_loan_not_found(self, mock_text, mock_engine):
        # Mock the loan details query result
        mock_result = MagicMock()
        mock_result.fetchone.return_value = None
        mock_engine.connect.return_value.__enter__ = mock_result

        # Call the generate_repayment_schedule function
        with self.assertRaises(ValueError):
            generate_repayment_schedule(self.loan_id)

    @patch('config.engine')
    @patch('sqlalchemy.sql.expression.Text')
    def test_generate_repayment_schedule_zero_loan_term(self, mock_text, mock_engine):
        # Mock the loan details query result
        mock_result = MagicMock()
        mock_result.fetchone.return_value = (self.loan_amount, self.interest_rate, 0, self.start_date)
        mock_engine.connect.return_value.__enter__ = mock_result

        # Call the generate_repayment_schedule function
        with self.assertRaises(ValueError):
            generate_repayment_schedule(self.loan_id)

if __name__ == '__main__':
    unittest.main()
