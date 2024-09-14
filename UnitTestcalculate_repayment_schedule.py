
import unittest
from your_module import calculate_repayment_schedule  # Replace with the actual module name
import pandas as pd
from sqlalchemy import text
import psycopg2

class TestCalculateRepaymentSchedule(unittest.TestCase):
    def setUp(self):
        # Create a test database connection
        self.conn = psycopg2.connect(
            dbname="your_database_name",
            user="your_username",
            password="your_password",
            host="your_host",
            port="your_port"
        )
        self.conn.autocommit = True

    def tearDown(self):
        # Close the test database connection
        self.conn.close()

    def test_loan_id_not_found(self):
        # Test when loan ID is not found in the database
        loan_id = 9999  # Replace with a non-existent loan ID
        result = calculate_repayment_schedule(loan_id)
        self.assertIsNone(result)

    def test_valid_loan_id(self):
        # Test with a valid loan ID
        loan_id = 1  # Replace with an existing loan ID
        result = calculate_repayment_schedule(loan_id)
        self.assertIsInstance(result, pd.DataFrame)
        self.assertGreaterEqual(len(result), 1)

    def test_zero_loan_amount(self):
        # Test when loan amount is zero
        loan_id = 1  # Replace with an existing loan ID
        # Update loan amount to zero in the database
        query = "UPDATE loans SET loanamount = 0 WHERE loanid = :loan_id"
        self.conn.execute(query, {'loan_id': loan_id})
        result = calculate_repayment_schedule(loan_id)
        self.assertIsNone(result)

    def test_negative_loan_amount(self):
        # Test when loan amount is negative
        loan_id = 1  # Replace with an existing loan ID
        # Update loan amount to negative in the database
        query = "UPDATE loans SET loanamount = -100 WHERE loanid = :loan_id"
        self.conn.execute(query, {'loan_id': loan_id})
        with self.assertRaises(ValueError):
            calculate_repayment_schedule(loan_id)

    def test_invalid_interest_rate(self):
        # Test when interest rate is invalid (e.g., negative or zero)
        loan_id = 1  # Replace with an existing loan ID
        # Update interest rate to invalid value in the database
        query = "UPDATE loans SET interestrate = -1 WHERE loanid = :loan_id"
        self.conn.execute(query, {'loan_id': loan_id})
        with self.assertRaises(ValueError):
            calculate_repayment_schedule(loan_id)

    def test_zero_loan_term(self):
        # Test when loan term is zero
        loan_id = 1  # Replace with an existing loan ID
        # Update loan term to zero in the database
        query = "UPDATE loans SET loanterm = 0 WHERE loanid = :loan_id"
        self.conn.execute(query, {'loan_id': loan_id})
        with self.assertRaises(ValueError):
            calculate_repayment_schedule(loan_id)

    def test_negative_loan_term(self):
        # Test when loan term is negative
        loan_id = 1  # Replace with an existing loan ID
        # Update loan term to negative in the database
        query = "UPDATE loans SET loanterm = -1 WHERE loanid = :loan_id"
        self.conn.execute(query, {'loan_id': loan_id})
        with self.assertRaises(ValueError):
            calculate_repayment_schedule(loan_id)

if __name__ == '__main__':
    unittest.main()
