
import unittest
from unittest.mock import patch, DEFAULT
from your_module import calculate_repayment_schedule
import pandas as pd
import sqlite3
from your_module import engine

class TestCalculateRepaymentSchedule(unittest.TestCase):

    @patch('your_module.engine')
    def test_calculate_repayment_schedule(self, mock_engine):
        mock_conn = mock_engine.connect.return_value
        mock_cursor = mock_conn.execute.return_value

        calculate_repayment_schedule(1)

        mock_engine.connect.assert_called_once()
        mock_conn.execute.assert_called_once()
        mock_conn.execute().fetchall.assert_called_once()
        mock_cursor.fetchall.assert_called_once()

        # get connection and cursor objects
        conn = engine.connect()
        cursor = conn.execute()
        
        # Close the connection
        conn.close()
        
    def test_invalid_loan_id(self):
        with self.assertRaises(sqlite3.Error):
            calculate_repayment_schedule(0)

    def test_start_date_is_start_of_month(self):
        loan_details = [(10000.0, 5.0, 30, '2022-01-01')]
        calculate_repayment_schedule(1)
        payment_date = '2022-01-01'
        for i in range(2, 31):
            payment_date = pd.to_datetime(payment_date)
            payment_date += pd.Timedelta(days=1)
            payment_date = payment_date.strftime('%Y-%m-%d')
        assert payment_date

    def test_start_date_is_middle_of_month(self):
        loan_details = [(10000.0, 5.0, 30, '2022-01-15')]
        calculate_repayment_schedule(1)
        payment_date = '2022-01-15'
        for i in range(3, 31):
            payment_date = pd.to_datetime(payment_date)
            payment_date += pd.Timedelta(days=1)
            payment_date = payment_date.strftime('%Y-%m-%d')
        assert payment_date

    def test_payment_date_is_at_the_end_of_month(self):
        loan_details = [(10000.0, 5.0, 30, '2022-02-28')]
        calculate_repayment_schedule(1)
        payment_date = '2022-02-28'
        for i in range(29, 28, -1):
            payment_date = pd.to_datetime(payment_date)
            payment_date += pd.Timedelta(days=1)
            payment_date = payment_date.strftime('%Y-%m-%d')
        assert payment_date

    def test_total_repayment_is_not_exceeding_loan_amount(self):
        loan_details = [(10000.0, 5.0, 30, '2022-01-01')]
        calculate_repayment_schedule(1)
        total_repayment = cursor.execute(text("SELECT totalpayment FROM repaymentschedule WHERE loanid = :loan_id"), 
                                 {'loan_id': 1}).fetchall()
        self.assertLessEqual(total_repayment[0][0], 10000.0)

    def test_total_repayment_is_exceeding_loan_amount(self):
        loan_details = [(10000.0, 5.0, 30, '2022-01-01')]
        calculate_repayment_schedule(1)
        total_repayment = cursor.execute(text("SELECT totalpayment FROM repaymentschedule WHERE loanid = :loan_id"), 
                                 {'loan_id': 1}).fetchall()
        self.assertGreaterEqual(total_repayment[0][0], 10000.0)

    def test_final_balance_is_zero(self):
        loan_details = [(1000.0, 5.0, 1, '2022-01-01')]
        calculate_repayment_schedule(1)
        final_balance = cursor.execute(text("SELECT balance FROM repaymentschedule WHERE loanid = :loan_id ORDER BY paymentdate desc LIMIT 1"), 
                                 {'loan_id': 1}).fetchall()
        self.assertEqual(final_balance[0][0], 0)

    def test_final_balance_is_not_zero(self):
        loan_details = [(1000.0, 5.0, 1, '2022-01-01')]
        calculate_repayment_schedule(1)
        final_balance = cursor.execute(text("SELECT balance FROM repaymentschedule WHERE loanid = :loan_id ORDER BY paymentdate desc LIMIT 1"), 
                                 {'loan_id': 1}).fetchall()
        self.assertNotEqual(final_balance[0][0], 0)

if __name__ == '__main__':
    unittest.main()
