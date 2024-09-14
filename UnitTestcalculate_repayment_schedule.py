
import unittest
from your_module import generate_repayment_schedule

class TestGenerateRepaymentSchedule(unittest.TestCase):
    def setUp(self):
        # Create a test database connection
        self.conn = engine.connect()

    def tearDown(self):
        # Close the test database connection
        self.conn.close()

    def test_success(self):
        # Test with valid loan ID
        loan_id = 1
        result = generate_repayment_schedule(loan_id)
        self.assertEqual(result, "Repayment schedule generated successfully")

    def test_invalid_loan_id(self):
        # Test with invalid loan ID
        loan_id = -1
        with self.assertRaises(psycopg2.Error):
            generate_repayment_schedule(loan_id)

    def test_loan_id_not_found(self):
        # Test with loan ID that doesn't exist in the database
        loan_id = 1000
        with self.assertRaises(psycopg2.Error):
            generate_repayment_schedule(loan_id)

    def test_loan_details_failure(self):
        # Test with a loan ID that has invalid details (e.g. NULL values)
        loan_id = 2
        # Simulate a database error by setting the loan details to None
        with patch.object(self.conn, 'execute', return_value=None):
            with self.assertRaises(psycopg2.Error):
                generate_repayment_schedule(loan_id)

    def test_repayment_schedule_failure(self):
        # Test with a loan ID that fails to insert into the RepaymentSchedule table
        loan_id = 3
        # Simulate a database error by raising an exception on insert
        with patch.object(self.conn, 'execute', side_effect=psycopg2.Error):
            with self.assertRaises(psycopg2.Error):
                generate_repayment_schedule(loan_id)

if __name__ == '__main__':
    unittest.main()
