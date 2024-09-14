
import unittest
from your_module import generate_repayment_schedule  # Replace with the actual module name

class TestGenerateRepaymentSchedule(unittest.TestCase):
    def setUp(self):
        # Create a test database connection
        self.conn = engine.connect()

    def tearDown(self):
        # Close the test database connection
        self.conn.close()

    def test_loan_found(self):
        # Test case: loan found, valid repayment schedule generated
        loan_id = 1  # Replace with an existing loan ID in the test database
        repayment_schedule = generate_repayment_schedule(loan_id)
        self.assertIsNotNone(repayment_schedule)
        self.assertIsInstance(repayment_schedule, pd.DataFrame)
        self.assertGreater(len(repayment_schedule), 0)

    def test_loan_not_found(self):
        # Test case: loan not found, None returned
        loan_id = 999  # Replace with a non-existing loan ID in the test database
        repayment_schedule = generate_repayment_schedule(loan_id)
        self.assertIsNone(repayment_schedule)

    def test_invalid_loan_id(self):
        # Test case: invalid loan ID, error raised
        loan_id = "invalid"  # Replace with an invalid loan ID
        with self.assertRaises(TypeError):
            generate_repayment_schedule(loan_id)

    def test_zero_interest_rate(self):
        # Test case: zero interest rate, repayment schedule generated
        loan_id = 2  # Replace with a loan ID with zero interest rate in the test database
        repayment_schedule = generate_repayment_schedule(loan_id)
        self.assertIsNotNone(repayment_schedule)
        self.assertIsInstance(repayment_schedule, pd.DataFrame)
        self.assertGreater(len(repayment_schedule), 0)

    def test_negative_interest_rate(self):
        # Test case: negative interest rate, error raised
        loan_id = 3  # Replace with a loan ID with negative interest rate in the test database
        with self.assertRaises(ValueError):
            generate_repayment_schedule(loan_id)

    def test_invalid_loan_term(self):
        # Test case: invalid loan term, error raised
        loan_id = 4  # Replace with a loan ID with invalid loan term in the test database
        with self.assertRaises(ValueError):
            generate_repayment_schedule(loan_id)

    def test_database_error(self):
        # Test case: database error, error message printed
        loan_id = 5  # Replace with a loan ID that causes a database error
        with self.assertRaises(psycopg2.Error):
            generate_repayment_schedule(loan_id)

if __name__ == "__main__":
    unittest.main()
