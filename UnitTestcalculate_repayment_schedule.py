
import unittest
from unittest.mock import patch, Mock
from datetime import datetime, timedelta
from loan_calculator import calculate_repayment_schedule
from config import engine

class TestLoanCalculator(unittest.TestCase):

    @patch('config.engine')
    @patch('psycopg2')
    @patch('sqlalchemy.engine')
    def test_calculate_repayscale_not_found(self, mock_sqlalchemy_engine, mock_psycopg2, mock_engine):
        loan_id = 'abc'
        mock_engine.execute.return_value = None
        result = calculate_repayment_schedule(loan_id)
        self.assertEqual(result, [])

    @patch('config.engine')
    @patch('psycopg2')
    @patch('sqlalchemy.engine')
    def test_calculate_repayscale_found(self, mock_sqlalchemy_engine, mock_psycopg2, mock_engine):
        loan_id = 'abc'
        loan_amount = 100000
        interest_rate = 10
        loan_term = 60
        start_date = datetime(2020, 1, 1)
        mock_engine.execute.return_value = (loan_amount, interest_rate, loan_term, start_date)
        result = calculate_repayment_schedule(loan_id)
        self.assertEqual(result, [])

    @patch('config.engine')
    @patch('psycopg2')
    @patch('sqlalchemy.engine')
    def test_calculate_repayscale_invalid_input(self, mock_sqlalchemy_engine, mock_psycopg2, mock_engine):
        loan_id = 'abc'
        mock_engine.execute.return_value = (None, None, None, None)
        with self.assertRaises(Exception):
            calculate_repayment_schedule(loan_id)

    @patch('config.engine')
    @patch('psycopg2')
    @patch('sqlalchemy.engine')
    def test_calculate_repayscale_zero_loan_term(self, mock_sqlalchemy_engine, mock_psycopg2, mock_engine):
        loan_id = 'abc'
        loan_amount = 100000
        interest_rate = 10
        loan_term = 0
        start_date = datetime(2020, 1, 1)
        mock_engine.execute.return_value = (loan_amount, interest_rate, loan_term, start_date)
        result = calculate_repayment_schedule(loan_id)
        self.assertEqual(result, [])

    @patch('config.engine')
    @patch('psycopg2')
    @patch('sqlalchemy.engine')
    def test_calculate_repayscale_zero_loan_amount(self, mock_sqlalchemy_engine, mock_psycopg2, mock_engine):
        loan_id = 'abc'
        loan_amount = 0
        interest_rate = 10
        loan_term = 60
        start_date = datetime(2020, 1, 1)
        mock_engine.execute.return_value = (loan_amount, interest_rate, loan_term, start_date)
        result = calculate_repayment_schedule(loan_id)
        self.assertEqual(result, [])

if __name__ == '__main__':
    unittest.main()
