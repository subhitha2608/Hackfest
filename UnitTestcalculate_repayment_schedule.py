
import unittest
from your_module import generate_repayment_schedule

class TestGenerateRepaymentSchedule(unittest.TestCase):
    def test_loan_id_1(self):
        loan_id = 1
        repayment_schedule = generate_repayment_schedule(loan_id)
        self.assertIsInstance(repayment_schedule, pd.DataFrame)
        self.assertEqual(repayment_schedule.shape[0], 12)  # assuming 12 months loan term
        self.assertEqual(repayment_schedule.iloc[0]['loan_id'], loan_id)
        self.assertEqual(repayment_schedule.iloc[0]['payment_number'], 1)
        self.assertGreater(repayment_schedule.iloc[0]['total_payment'], 0)

    def test_loan_id_2(self):
        loan_id = 2
        repayment_schedule = generate_repayment_schedule(loan_id)
        self.assertIsInstance(repayment_schedule, pd.DataFrame)
        self.assertEqual(repayment_schedule.shape[0], 24)  # assuming 24 months loan term
        self.assertEqual(repayment_schedule.iloc[0]['loan_id'], loan_id)
        self.assertEqual(repayment_schedule.iloc[0]['payment_number'], 1)
        self.assertGreater(repayment_schedule.iloc[0]['total_payment'], 0)

    def test_invalid_loan_id(self):
        loan_id = 999  # assuming this loan id does not exist
        with self.assertRaises(Exception):
            generate_repayment_schedule(loan_id)

if __name__ == '__main__':
    unittest.main()
