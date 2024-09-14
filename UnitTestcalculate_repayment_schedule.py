
import unittest
from your_module import generate_repayment_schedule  # Replace with the actual module name
import pandas as pd

class TestGenerateRepaymentSchedule(unittest.TestCase):
    def setUp(self):
        # Create a test engine and database connection
        self.engine = create_engine('postgresql://user:password@host:port/dbname')
        self.conn = self.engine.connect()

        # Create test data in the loans table
        self.loan_id = 1
        self.loan_amount = 10000
        self.interest_rate = 5
        self.loan_term = 60
        self.start_date = pd.Timestamp('2022-01-01')
        self.conn.execute("""
            INSERT INTO loans (loanid, loanamount, interestrate, loanterm, startdate)
            VALUES (%s, %s, %s, %s, %s)
        """, (self.loan_id, self.loan_amount, self.interest_rate, self.loan_term, self.start_date))

    def tearDown(self):
        # Clean up test data
        self.conn.execute("DELETE FROM loans WHERE loanid = %s", (self.loan_id,))
        self.conn.close()

    def test_generate_repayment_schedule_valid_loan_id(self):
        # Test with a valid loan ID
        generate_repayment_schedule(self.loan_id)
        # Check that the repayment schedule was generated correctly
        self.conn.execute("SELECT COUNT(*) FROM repaymentschedule WHERE loanid = %s", (self.loan_id,))
        count = self.conn.fetchone()[0]
        self.assertEqual(count, self.loan_term)

    def test_generate_repayment_schedule_invalid_loan_id(self):
        # Test with an invalid loan ID
        with self.assertRaises(psycopg2.Error):
            generate_repayment_schedule(999)

    def test_generate_repayment_schedule_zero_loan_amount(self):
        # Test with a loan amount of 0
        self.conn.execute("UPDATE loans SET loanamount = 0 WHERE loanid = %s", (self.loan_id,))
        with self.assertRaises(ZeroDivisionError):
            generate_repayment_schedule(self.loan_id)

    def test_generate_repayment_schedule_negative_loan_amount(self):
        # Test with a negative loan amount
        self.conn.execute("UPDATE loans SET loanamount = -1000 WHERE loanid = %s", (self.loan_id,))
        with self.assertRaises(ValueError):
            generate_repayment_schedule(self.loan_id)

    def test_generate_repayment_schedule_zero_interest_rate(self):
        # Test with an interest rate of 0
        self.conn.execute("UPDATE loans SET interestrate = 0 WHERE loanid = %s", (self.loan_id,))
        with self.assertRaises(ZeroDivisionError):
            generate_repayment_schedule(self.loan_id)

    def test_generate_repayment_schedule_negative_interest_rate(self):
        # Test with a negative interest rate
        self.conn.execute("UPDATE loans SET interestrate = -5 WHERE loanid = %s", (self.loan_id,))
        with self.assertRaises(ValueError):
            generate_repayment_schedule(self.loan_id)

    def test_generate_repayment_schedule_zero_loan_term(self):
        # Test with a loan term of 0
        self.conn.execute("UPDATE loans SET loanterm = 0 WHERE loanid = %s", (self.loan_id,))
        with self.assertRaises(ZeroDivisionError):
            generate_repayment_schedule(self.loan_id)

    def test_generate_repayment_schedule_negative_loan_term(self):
        # Test with a negative loan term
        self.conn.execute("UPDATE loans SET loanterm = -60 WHERE loanid = %s", (self.loan_id,))
        with self.assertRaises(ValueError):
            generate_repayment_schedule(self.loan_id)

if __name__ == '__main__':
    unittest.main()
