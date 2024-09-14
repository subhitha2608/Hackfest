
import unittest
from your_module import generate_repayment_schedule

class TestGenerateRepaymentSchedule(unittest.TestCase):
    def setUp(self):
        # Create a test database connection
        self.conn = engine.connect()

    def tearDown(self):
        # Close the test database connection
        self.conn.close()

    def test_valid_loan_id(self):
        # Test with a valid loan ID
        loan_id = 1
        repayment_schedule = generate_repayment_schedule(loan_id)
        self.assertIsInstance(repayment_schedule, pd.DataFrame)
        self.assertGreater(len(repayment_schedule), 0)

    def test_invalid_loan_id(self):
        # Test with an invalid loan ID
        loan_id = 9999
        with self.assertRaises(psycopg2.Error):
            generate_repayment_schedule(loan_id)

    def test_loan_id_none(self):
        # Test with a None loan ID
        loan_id = None
        with self.assertRaises(TypeError):
            generate_repayment_schedule(loan_id)

    def test_loan_id_zero(self):
        # Test with a loan ID of 0
        loan_id = 0
        with self.assertRaises(psycopg2.Error):
            generate_repayment_schedule(loan_id)

    def test_repayment_schedule_columns(self):
        # Test that the repayment schedule has the correct columns
        loan_id = 1
        repayment_schedule = generate_repayment_schedule(loan_id)
        expected_columns = ['loanid', 'paymentnumber', 'paymentdate', 'principalamount', 'interestamount', 'totalpayment', 'balance']
        self.assertListEqual(list(repayment_schedule.columns), expected_columns)

    def test_repayment_schedule_data(self):
        # Test that the repayment schedule has the correct data
        loan_id = 1
        repayment_schedule = generate_repayment_schedule(loan_id)
        self.assertGreater(len(repayment_schedule), 0)
        self.assertAlmostEqual(repayment_schedule.iloc[0]['totalpayment'], 500.0, places=2)  # example value

if __name__ == '__main__':
    unittest.main()
