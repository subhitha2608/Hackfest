
import unittest
from your_module import generate_repayment_schedule  # Replace with the actual module name

class TestGenerateRepaymentSchedule(unittest.TestCase):
    def test_loan_found(self):
        loan_id = 1
        repayment_schedule = generate_repayment_schedule(loan_id)
        self.assertIsNotNone(repayment_schedule)
        self.assertIsInstance(repayment_schedule, pd.DataFrame)

    def test_loan_not_found(self):
        loan_id = 999  # Assuming this loan ID does not exist in the database
        with self.assertRaises(Exception):
            generate_repayment_schedule(loan_id)

    def test_repayment_schedule_columns(self):
        loan_id = 1
        repayment_schedule = generate_repayment_schedule(loan_id)
        expected_columns = ['loanid', 'paymentnumber', 'paymentdate', 'principalamount', 'interestamount', 'totalpayment', 'balance']
        self.assertEqual(list(repayment_schedule.columns), expected_columns)

    def test_repayment_schedule_data(self):
        loan_id = 1
        repayment_schedule = generate_repayment_schedule(loan_id)
        self assertedGreater(len(repayment_schedule), 0)  # Assuming the loan has more than one payment
        self.assertAlmostEqual(repayment_schedule.iloc[0]['balance'], 1000.0, places=2)  # Assuming the initial balance is 1000.0
        self.assertAlmostEqual(repayment_schedule.iloc[-1]['balance'], 0.0, places=2)  # Assuming the final balance is 0.0

if __name__ == '__main__':
    unittest.main()
