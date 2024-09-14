
import unittest
from your_module import generate_repayment_schedule  # Replace 'your_module' with the actual module name
import pandas as pd
from datetime import datetime, timedelta
import psycopg2
from sqlalchemy import text, create_engine

class TestGenerateRepaymentSchedule(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.engine = create_engine('postgresql://user:password@host:port/dbname')  # Replace with your DB credentials
        cls.conn = cls.engine.raw_connection()

    def test_generate_repayment_schedule(self):
        loan_id = 1
        loan_amount = 10000
        interest_rate = 6
        loan_term = 12
        start_date = datetime(2022, 1, 1)

        # Create a test loan
        query = text("""
            INSERT INTO loans (loanid, loanamount, interestrate, loanterm, startdate)
            VALUES (:loan_id, :loan_amount, :interest_rate, :loan_term, :start_date)
            RETURNING loanid
        """)
        result = self.engine.execute(query, {
            'loan_id': loan_id,
            'loan_amount': loan_amount,
            'interest_rate': interest_rate,
            'loan_term': loan_term,
            'start_date': start_date
        })
        result.fetchall()

        generate_repayment_schedule(loan_id)

        # Check repayment schedule
        query = text("""
            SELECT COUNT(*) 
            FROM repaymentschedule 
            WHERE loanid = :loan_id
        """)
        result = self.engine.execute(query, {'loan_id': loan_id})
        count, = result.fetchone()
        self.assertEqual(count, loan_term)

    def test_generate_repayment_schedule_zero_interest_rate(self):
        loan_id = 2
        loan_amount = 10000
        interest_rate = 0
        loan_term = 12
        start_date = datetime(2022, 1, 1)

        # Create a test loan
        query = text("""
            INSERT INTO loans (loanid, loanamount, interestrate, loanterm, startdate)
            VALUES (:loan_id, :loan_amount, :interest_rate, :loan_term, :start_date)
            RETURNING loanid
        """)
        result = self.engine.execute(query, {
            'loan_id': loan_id,
            'loan_amount': loan_amount,
            'interest_rate': interest_rate,
            'loan_term': loan_term,
            'start_date': start_date
        })
        result.fetchall()

        generate_repayment_schedule(loan_id)

        # Check repayment schedule
        query = text("""
            SELECT COUNT(*) 
            FROM repaymentschedule 
            WHERE loanid = :loan_id
        """)
        result = self.engine.execute(query, {'loan_id': loan_id})
        count, = result.fetchone()
        self.assertEqual(count, loan_term)

    def test_generate_repayment_schedule_one_month_loan_term(self):
        loan_id = 3
        loan_amount = 10000
        interest_rate = 6
        loan_term = 1
        start_date = datetime(2022, 1, 1)

        # Create a test loan
        query = text("""
            INSERT INTO loans (loanid, loanamount, interestrate, loanterm, startdate)
            VALUES (:loan_id, :loan_amount, :interest_rate, :loan_term, :start_date)
            RETURNING loanid
        """)
        result = self.engine.execute(query, {
            'loan_id': loan_id,
            'loan_amount': loan_amount,
            'interest_rate': interest_rate,
            'loan_term': loan_term,
            'start_date': start_date
        })
        result.fetchall()

        generate_repayment_schedule(loan_id)

        # Check repayment schedule
        query = text("""
            SELECT COUNT(*) 
            FROM repaymentschedule 
            WHERE loanid = :loan_id
        """)
        result = self.engine.execute(query, {'loan_id': loan_id})
        count, = result.fetchone()
        self.assertEqual(count, loan_term)

    def test_generate_repayment_schedule_invalid_loan_id(self):
        loan_id = 999  # Non-existent loan ID
        with self.assertRaises(Exception):
            generate_repayment_schedule(loan_id)

    def tearDown(self):
        # Clean up test data
        query = text("""
            DELETE FROM repaymentschedule WHERE loanid IN (1, 2, 3)
        """)
        self.engine.execute(query)
        query = text("""
            DELETE FROM loans WHERE loanid IN (1, 2, 3)
        """)
        self.engine.execute(query)
        self.conn.commit()

if __name__ == '__main__':
    unittest.main()
