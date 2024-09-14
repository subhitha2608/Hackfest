
import unittest
from your_module import calculate_repayment_schedule
import pandas as pd

class TestCalculateRepaymentSchedule(unittest.TestCase):
    def setUp(self):
        # Create a test database connection
        self.conn = engine.connect()

        # Create test data in the loans table
        query = text("""
            INSERT INTO loans (loanid, loanamount, interestrate, loanterm, startdate)
            VALUES (1, 10000, 6, 60, '2022-01-01')
        """)
        self.conn.execute(query)
        self.conn.commit()

    def tearDown(self):
        # Clean up test data
        query = text("DELETE FROM loans WHERE loanid = 1")
        self.conn.execute(query)
        self.conn.commit()
        self.conn.close()

    def test_calculate_repayment_schedule_valid_loan_id(self):
        loan_id = 1
        repayment_schedule = calculate_repayment_schedule(loan_id)
        self.assertIsInstance(repayment_schedule, pd.DataFrame)
        self.assertEqual(repayment_schedule.shape[0], 60)  # 60 months
        self.assertEqual(repayment_schedule['loanid'].iloc[0], loan_id)

    def test_calculate_repayment_schedule_invalid_loan_id(self):
        loan_id = 2  # non-existent loan ID
        with self.assertRaises(Exception):
            calculate_repayment_schedule(loan_id)

    def test_calculate_repayment_schedule_zero_loan_amount(self):
        # Update test data with zero loan amount
        query = text("UPDATE loans SET loanamount = 0 WHERE loanid = 1")
        self.conn.execute(query)
        self.conn.commit()

        loan_id = 1
        with self.assertRaises(ZeroDivisionError):
            calculate_repayment_schedule(loan_id)

    def test_calculate_repayment_schedule_null_interest_rate(self):
        # Update test data with null interest rate
        query = text("UPDATE loans SET interestrate = NULL WHERE loanid = 1")
        self.conn.execute(query)
        self.conn.commit()

        loan_id = 1
        with self.assertRaises(TypeError):
            calculate_repayment_schedule(loan_id)

    def test_calculate_repayment_schedule_negative_loan_term(self):
        # Update test data with negative loan term
        query = text("UPDATE loans SET loanterm = -1 WHERE loanid = 1")
        self.conn.execute(query)
        self.conn.commit()

        loan_id = 1
        with self.assertRaises(ValueError):
            calculate_repayment_schedule(loan_id)

if __name__ == '__main__':
    unittest.main()
