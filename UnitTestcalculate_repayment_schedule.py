
import unittest
from your_module import generate_repayment_schedule
from sqlalchemy import create_engine
import psycopg2
import pandas as pd

class TestGenerateRepaymentSchedule(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.engine = create_engine('postgresql://user:password@host:port/dbname')
        cls.conn = cls.engine.connect()

    @classmethod
    def tearDownClass(cls):
        cls.conn.close()

    def test_generate_repayment_schedule_success(self):
        loan_id = 1
        generate_repayment_schedule(loan_id)

        # Check if repayment schedule is generated correctly
        query = "SELECT * FROM repaymentschedule WHERE loanid = :loan_id"
        result = self.conn.execute(query, {'loan_id': loan_id})
        rows = result.fetchall()
        self assertGreater(len(rows), 0)

    def test_generate_repayment_schedule_invalid_loan_id(self):
        loan_id = -1
        with self.assertRaises(psycopg2.Error):
            generate_repayment_schedule(loan_id)

    def test_generate_repayment_schedule_loan_not_found(self):
        loan_id = 1000  # assume this loan id does not exist
        with self.assertRaises(TypeError):
            generate_repayment_schedule(loan_id)

    def test_generate_repayment_schedule_zero_interest_rate(self):
        loan_id = 2  # assume this loan has 0 interest rate
        generate_repayment_schedule(loan_id)

        # Check if repayment schedule is generated correctly
        query = "SELECT * FROM repaymentschedule WHERE loanid = :loan_id"
        result = self.conn.execute(query, {'loan_id': loan_id})
        rows = result.fetchall()
        self assertGreater(len(rows), 0)

    def test_generate_repayment_schedule_negative_loan_amount(self):
        loan_id = 3  # assume this loan has negative loan amount
        with self.assertRaises(ValueError):
            generate_repayment_schedule(loan_id)

if __name__ == '__main__':
    unittest.main()
