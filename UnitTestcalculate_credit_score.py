Python
import unittest
from your_module import update_credit_score

class TestUpdateCreditScore(unittest.TestCase):

    def setUp(self):
        self.customer_id = 1

    def test_update_credit_score_positive_total_loan_amount(self):
        total_loan_amount = 1000
        total_repayment = 500
        outstanding_loan_balance = 200
        credit_card_balance = 0
        late_pay_count = 0
        v_credit_score = update_credit_score(self.customer_id)
        self.assertEqual(v_credit_score, 700)

    def test_update_credit_score_negative_total_loan_amount(self):
        total_loan_amount = -1000
        total_repayment = 500
        outstanding_loan_balance = -200
        credit_card_balance = 0
        late_pay_count = 0
        v_credit_score = update_credit_score(self.customer_id)
        self.assertEqual(v_credit_score, 400)

    def test_update_credit_score_zero_total_loan_amount(self):
        total_loan_amount = 0
        total_repayment = 0
        outstanding_loan_balance = 0
        credit_card_balance = 0
        late_pay_count = 0
        v_credit_score = update_credit_score(self.customer_id)
        self.assertEqual(v_credit_score, 400)

    def test_update_credit_score_non_zero_credit_card_balance(self):
        total_loan_amount = 1000
        total_repayment = 500
        outstanding_loan_balance = 200
        credit_card_balance = 5000
        late_pay_count = 0
        v_credit_score = update_credit_score(self.customer_id)
        self.assertEqual(v_credit_score, 550)

    def test_update_credit_score_non_zero_late_pay_count(self):
        total_loan_amount = 1000
        total_repayment = 500
        outstanding_loan_balance = 200
        credit_card_balance = 0
        late_pay_count = 5
        v_credit_score = update_credit_score(self.customer_id)
        self.assertEqual(v_credit_score, 350)

    def test_update_credit_score_below_threshold(self):
        total_loan_amount = 0
        total_repayment = 0
        outstanding_loan_balance = 0
        credit_card_balance = 0
        late_pay_count = 10
        v_credit_score = update_credit_score(self.customer_id)
        self.assertEqual(v_credit_score, 300)

    def test_update_credit_score_above_threshold(self):
        total_loan_amount = 1000
        total_repayment = 1000
        outstanding_loan_balance = 0
        credit_card_balance = 0
        late_pay_count = 0
        v_credit_score = update_credit_score(self.customer_id)
        self.assertEqual(v_credit_score, 850)

if __name__ == '__main__':
    unittest.main()
