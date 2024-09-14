
import unittest
from datetime import datetime, timedelta
from decimal import Decimal

class TestCalculateRepaymentSchedule(unittest.TestCase):

    def setUp(self):
        self.engine = engine
        self.loan_id = 1

    def test_calculate_repayment_schedule(self):
        calculate_repayment_schedule(self.loan_id)

    def test_loan_amount_missing(self):
        with self.assertRaises/IndexError:
            loan_amount = pd.read_sql_query(text("SELECT loanamount FROM loans WHERE loanid = :loan_id"), self.engine, params={'loan_id': self.loan_id}).iloc[0]['loanamount']
            calculate_repayment_schedule(self.loan_id)

    def test_interest_rate_zero(self):
        start_date = datetime.now()
        loan_amount = Decimal(1000.0)
        interest_rate = Decimal(0.0)
        loan_term = 12
        calculate_repayment_schedule(self.loan_id)
        self.assertEqual(len(pd.read_sql_query(text("SELECT * FROM repaymentschedule WHERE loanid = :loan_id"), self.engine, params={'loan_id': self.loan_id})), loan_term)
        self.assertEqual(loan_amount, Decimal(0.0))

    def test_loan_term_zero(self):
        loan_amount = Decimal(1000.0)
        interest_rate = Decimal(5.0)
        start_date = datetime.now()
        loan_term = 0
        with self.assertRaises(IndexError):
            calculate_repayment_schedule(self.loan_id)

    def test_start_date_missing(self):
        loan_amount = Decimal(1000.0)
        interest_rate = Decimal(5.0)
        loan_term = 12
        with self.assertRaises(IndexError):
            calculate_repayment_schedule(self.loan_id)

    def test_invalid_loan_term(self):
        start_date = datetime.now()
        loan_amount = Decimal(1000.0)
        interest_rate = Decimal(5.0)
        loan_term = -1
        with self.assertRaises(ValueError):
            calculate_repayment_schedule(self.loan_id)

    def test_invalid_interest_rate(self):
        start_date = datetime.now()
        loan_amount = Decimal(1000.0)
        interest_rate = -1
        loan_term = 12
        with self.assertRaises(ValueError):
            calculate_repayment_schedule(self.loan_id)

if __name__ == '__main__':
    unittest.main()
