
import unittest
from your_module import calculate_repayment_schedule
import pandas as pd

class TestCalculateRepaymentSchedule(unittest.TestCase):
    def setUp(self):
        # Create a test engine and connection
        self.engine = create_engine('postgresql://user:password@host:port/dbname')
        self.conn = self.engine.connect()

    def tearDown(self):
        # Close the connection
        self.conn.close()

    def test_loan_found(self):
        # Create a test loan in the loans table
        query = sa.text("INSERT INTO loans (loanid, loanamount, interestrate, loanterm, startdate) VALUES (1, 10000, 5, 36, '2022-01-01')")
        self.conn.execute(query)

        # Call the function
        repayment_schedule = calculate_repayment_schedule(1)

        # Assert the result is not None
        self.assertIsNotNone(repayment_schedule)

        # Assert the repayment schedule has the correct columns
        self.assertEqual(repayment_schedule.columns.tolist(), ['loan_id', 'payment_number', 'payment_date', 'principal_amount', 'interest_amount', 'total_payment', 'balance'])

        # Assert the repayment schedule has the correct number of rows
        self.assertEqual(len(repayment_schedule), 36)

    def test_loan_not_found(self):
        # Call the function with a non-existent loan ID
        repayment_schedule = calculate_repayment_schedule(2)

        # Assert the result is None
        self.assertIsNone(repayment_schedule)

    def test_zero_interest_rate(self):
        # Create a test loan in the loans table with 0% interest rate
        query = sa.text("INSERT INTO loans (loanid, loanamount, interestrate, loanterm, startdate) VALUES (1, 10000, 0, 36, '2022-01-01')")
        self.conn.execute(query)

        # Call the function
        repayment_schedule = calculate_repayment_schedule(1)

        # Assert the result is not None
        self.assertIsNotNone(repayment_schedule)

        # Assert the repayment schedule has the correct columns
        self.assertEqual(repayment_schedule.columns.tolist(), ['loan_id', 'payment_number', 'payment_date', 'principal_amount', 'interest_amount', 'total_payment', 'balance'])

        # Assert the repayment schedule has the correct number of rows
        self.assertEqual(len(repayment_schedule), 36)

    def test_negative_loan_amount(self):
        # Create a test loan in the loans table with a negative loan amount
        query = sa.text("INSERT INTO loans (loanid, loanamount, interestrate, loanterm, startdate) VALUES (1, -10000, 5, 36, '2022-01-01')")
        self.conn.execute(query)

        # Call the function
        with self.assertRaises(ValueError):
            calculate_repayment_schedule(1)

    def test_non_integer_loan_term(self):
        # Create a test loan in the loans table with a non-integer loan term
        query = sa.text("INSERT INTO loans (loanid, loanamount, interestrate, loanterm, startdate) VALUES (1, 10000, 5, 36.5, '2022-01-01')")
        self.conn.execute(query)

        # Call the function
        with self.assertRaises(ValueError):
            calculate_repayment_schedule(1)

if __name__ == '__main__':
    unittest.main()
