
import unittest
from your_module import generate_repayment_schedule

class TestGenerateRepaymentSchedule(unittest.TestCase):
    def test_loan_id_1(self):
        loan_id = 1
        repayment_schedule = generate_repayment_schedule(loan_id)
        self.assertEquals(repayment_schedule.shape[0], 12)  # assuming 12 months for loan_id 1

    def test_loan_id_2(self):
        loan_id = 2
        repayment_schedule = generate_repayment_schedule(loan_id)
        self.assertEquals(repayment_schedule.iloc[0]['paymentnumber'], 1)  # check payment number starts from 1

    def test_loan_id_3(self):
        loan_id = 3
        repayment_schedule = generate_repayment_schedule(loan_id)
        self.assertEquals(repayment_schedule.iloc[-1]['balance'], 0)  # check balance becomes 0 at the end of loan term

if __name__ == '__main__':
    unittest.main()
