
import unittest
from your_module import calculate_repayment_schedule

class TestCalculateRepaymentSchedule(unittest.TestCase):
    def setUp(self):
        # Create a test loan ID
        self.loan_id = 1

    def test_valid_loan_id(self):
        # Test with a valid loan ID
        repayment_schedule = calculate_repayment_schedule(self.loan_id)
        self.assertIsInstance(repayment_schedule, pd.DataFrame)
        self assertEqual(repayment_schedule.shape[0], 12)  # 12 months in a year
        self assertEqual(repayment_schedule.shape[1], 7)  # 7 columns in the repayment schedule

    def test_invalid_loan_id(self):
        # Test with an invalid loan ID
        with self.assertRaisesREGEX(Exception, "Loan not found"):
            calculate_repayment_schedule(-1)

    def test_no_loan_details(self):
        # Test when there are no loan details for the given loan ID
        with self.assertRaisesREGEX(Exception, "No loan details found"):
            calculate_repayment_schedule(999)  # assume this loan ID doesn't exist

    def test_insufficient_funds(self):
        # Test when the loan amount is 0
        with self.assertRaisesREGEX(ValueError, "Loan amount cannot be 0"):
            calculate_repayment_schedule(self.loan_id, loan_amount=0)

    def test_interest_rate_zero(self):
        # Test when the interest rate is 0
        with self.assertRaisesREGEX(ValueError, "Interest rate cannot be 0"):
            calculate_repayment_schedule(self.loan_id, interest_rate=0)

    def test_loan_term_zero(self):
        # Test when the loan term is 0
        with self.assertRaisesREGEX(ValueError, "Loan term cannot be 0"):
            calculate_repayment_schedule(self.loan_id, loan_term=0)

    def test_start_date_in_future(self):
        # Test when the start date is in the future
        with self.assertRaisesREGEX(ValueError, "Start date cannot be in the future"):
            calculate_repayment_schedule(self.loan_id, start_date=pd.Timestamp("2030-01-01"))

    def tearDown(self):
        # Clean up any resources used during the test
        pass

if __name__ == "__main__":
    unittest.main()
