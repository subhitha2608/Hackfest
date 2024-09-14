
import unittest
from your_module import generate_repayment_schedule  # Replace with the actual module name
import pandas as pd
from sqlalchemy import create_engine

class TestGenerateRepaymentSchedule(unittest.TestCase):
    def setUp(self):
        # Create a test database connection
        self.engine = create_engine('postgresql://user:password@host:port/dbname')
        self.conn = self.engine.connect()

        # Create test data in the loans table
        self.conn.execute(text("""
            INSERT INTO loans (loanid, loanamount, interestrate, loanterm, startdate)
            VALUES (1, 1000, 5, 12, '2022-01-01')
        """))

    def tearDown(self):
        # Clean up test data
        self.conn.execute(text("TRUNCATE TABLE loans, repaymentschedule"))
        self.conn.close()

    def test_generate_repayment_schedule_valid_loan_id(self):
        loan_id = 1
        result = generate_repayment_schedule(loan_id)
        self.assertIsInstance(result, pd.DataFrame)
        self.assertEqual(result.shape[0], 12)  # 12 months in the repayment schedule
        self.assertEqual(result.columns.tolist(), ['loanid', 'paymentnumber', 'paymentdate', 'principalamount', 'interestamount', 'totalpayment', 'balance'])

    def test_generate_repayment_schedule_invalid_loan_id(self):
        loan_id = 2
        with self.assertRaises(psycopg2.Error):
            generate_repayment_schedule(loan_id)

    def test_generate_repayment_schedule_loan_not_found(self):
        loan_id = 3
        with self.assertRaises(psycopg2.Error):
            generate_repayment_schedule(loan_id)

    def test_generate_repayment_schedule_db_error(self):
        # Simulate a database error
        self.conn.close()
        with self.assertRaises(psycopg2.Error):
            generate_repayment_schedule(1)

    def test_generate_repayment_schedule_non_numeric_loan_id(self):
        loan_id = 'abc'
        with self.assertRaises(TypeError):
            generate_repayment_schedule(loan_id)

if __name__ == '__main__':
    unittest.main()
