
import unittest
from your_module import calculate_repayment_schedule  # Replace 'your_module' with the actual module name
import sqlalchemy as sa
import pandas as pd
import psycopg2

class TestCalculateRepaymentSchedule(unittest.TestCase):
    def setUp(self):
        # Create a test database connection
        self.conn = engine.connect()

    def tearDown(self):
        # Close the test database connection
        self.conn.close()

    def test_valid_loan_id(self):
        # Test with a valid loan ID
        loan_id = 1
        result = calculate_repayment_schedule(loan_id)
        self.assertIsInstance(result, pd.DataFrame)
        self.assertGreater(len(result), 0)

    def test_invalid_loan_id(self):
        # Test with an invalid loan ID
        loan_id = -1
        with self.assertRaises(sa.exc.NoResultFound):
            calculate_repayment_schedule(loan_id)

    def test_loan_id_not_found(self):
        # Test with a loan ID that doesn't exist in the database
        loan_id = 999
        with self.assertRaises(sa.exc.NoResultFound):
            calculate_repayment_schedule(loan_id)

    def test_interest_rate_zero(self):
        # Test with a loan that has an interest rate of 0%
        loan_id = 2  # Assume loan ID 2 has an interest rate of 0%
        result = calculate_repayment_schedule(loan_id)
        self.assertIsInstance(result, pd.DataFrame)
        self.assertGreater(len(result), 0)

    def test_loan_term_zero(self):
        # Test with a loan that has a term of 0 months
        loan_id = 3  # Assume loan ID 3 has a term of 0 months
        with self.assertRaises(ZeroDivisionError):
            calculate_repayment_schedule(loan_id)

    def test_repayment_schedule_columns(self):
        # Test that the repayment schedule has the correct columns
        loan_id = 1
        result = calculate_repayment_schedule(loan_id)
        expected_columns = ['paymentnumber', 'paymentdate', 'principalamount', 'interestamount', 'totalpayment', 'balance']
        self.assertCountEqual(result.columns, expected_columns)

    def test_repayment_schedule_data(self):
        # Test that the repayment schedule has reasonable data
        loan_id = 1
        result = calculate_repayment_schedule(loan_id)
        self.assertGreater(result['principalamount'].sum(), 0)
        self.assertGreater(result['interestamount'].sum(), 0)
        self.assertGreater(result['totalpayment'].sum(), 0)

if __name__ == '__main__':
    unittest.main()
