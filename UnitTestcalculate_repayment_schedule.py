
import unittest
from your_module import generate_repayment_schedule

class TestGenerateRepaymentSchedule(unittest.TestCase):
    def test_loan_id_123(self):
        loan_id = 123
        repayment_schedule = generate_repayment_schedule(loan_id)
        self.assertEqual(repayment_schedule.shape[0], 36)  # 36 months for a 3-year loan

    def test_loan_id_456(self):
        loan_id = 456
        repayment_schedule = generate_repayment_schedule(loan_id)
        self.assertEqual(repayment_schedule.loc[0, 'principalamount'], 150.0)  # first month's principal amount

    def test_loan_id_789(self):
        loan_id = 789
        repayment_schedule = generate_repayment_schedule(loan_id)
        self.assertEqual(repayment_schedule.loc[-1, 'balance'], 0.0)  # final balance should be 0

if __name__ == '__main__':
    unittest.main()
