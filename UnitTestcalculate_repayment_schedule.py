
import unittest
from unittest.mock import patch, Mock
from datetime import datetime, timedelta

class TestCalculateRepaymentSchedule(unittest.TestCase):

    @patch('config.engine')
    def test_calculate_repayment_schedule(self, mock_engine):
        loan_id = 1
        loan_amount = 100000
        interest_rate = 6
        loan_term = 360
        start_date = datetime.now()

        with mock_engine.connect() as conn:
            conn.execute = Mock(return_value=[loan_amount, interest_rate/100/12, loan_term, start_date])

        calculate_repayment_schedule(loan_id)
        repayment_schedule_entries = [(1, 1, start_date, 0, 100000, 100000, 100000), 
                                       (1, 2, start_date + timedelta(days=30), 0, 1499.97, 100000, 89801.03), 
                                       (1, 3, start_date + timedelta(days=60), 0, 1499.97, 100000, 74801.06), 
                                       ...
                                       (1, 360, start_date + timedelta(days=35160), 0, 0, 100000, 0)]

        mock_engine.execute.assert_any_call("INSERT INTO repaymentschedule (loanid, paymentnumber, paymentdate, principalamount, interestamount, totalpayment, balance) VALUES (:loan_id, :payment_number, :payment_date, :principal_amount, :interest_amount, :monthly_payment, :balance)", 
                                             {"loan_id": 1, "payment_number": 1, "payment_date": start_date, "principal_amount": 0, "interest_amount": 500, "monthly_payment": 2679.68, "balance": 100000})
        mock_engine.execute.assert_any_call("INSERT INTO repaymentschedule (loanid, paymentnumber, paymentdate, principalamount, interestamount, totalpayment, balance) VALUES (:loan_id, :payment_number, :payment_date, :principal_amount, :interest_amount, :monthly_payment, :balance)", 
                                             {"loan_id": 1, "payment_number": 360, "payment_date": start_date + timedelta(days=35160), "principal_amount": 0, "interest_amount": 0, "monthly_payment": 2679.68, "balance": 0})
        mock_engine.commit.assert_called_once()

    @patch('config.engine')
    def test_calculate_repayment_schedule_no_loan_found(self, mock_engine):
        loan_id = 1
        with mock_engine.connect() as conn:
            conn.execute = Mock(return_value=None)
        
        self.assertRaises(IndexError, calculate_repayment_schedule, loan_id)
        mock_engine.execute.assert_called_once()

    @patch('config.engine')
    def test_calculate_repayment_schedule_database_error(self, mock_engine):
        loan_id = 1
        with mock_engine.connect() as conn:
            conn.execute = Mock(side_effect=Exception("Database Error"))
        
        self.assertRaises(Exception, calculate_repayment_schedule, loan_id)
        mock_engine.execute.assert_called_once()

    @patch('config.engine')
    def test_calculate_repayment_schedule_invalid_loan_term(self, mock_engine):
        loan_id = 1
        invalid_loan_term = -1
        with mock_engine.connect() as conn:
            conn.execute = Mock(return_value=[100000, 6/100/12, invalid_loan_term, datetime.now()])
        
        with self.assertRaises(IndexError):
            calculate_repayment_schedule(loan_id)
        mock_engine.execute.assert_called_once()

    @patch('config.engine')
    def test_calculate_repayment_schedule_invalid_interest_rate(self, mock_engine):
        loan_id = 1
        invalid_interest_rate = 12
        with mock_engine.connect() as conn:
            conn.execute = Mock(return_value=[100000, invalid_interest_rate/100/12, 360, datetime.now()])
        
        with self.assertRaises(IndexError):
            calculate_repayment_schedule(loan_id)
        mock_engine.execute.assert_called_once()

if __name__ == '__main__':
    unittest.main()
