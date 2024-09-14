Python
import unittest
from config import engine
import pandas as pd
from your_module import calculate_credit_score

class TestCalculateCreditScore(unittest.TestCase):

    def setUp(self):
        self.customer_id = 1
        self.total_loan_amount = 10000
        self.total_repayment = 5000
        self.outstanding_loan_balance = 3000
        self.credit_card_balance = 5000
        self.late_pay_count = 2

        engine.execute("INSERT INTO loans (customer_id, loan_amount, repayment_amount, outstanding_balance) VALUES (%s, %s, %s, %s)", (self.customer_id, self.total_loan_amount, self.total_repayment, self.outstanding_loan_balance))
        engine.execute("INSERT INTO credit_cards (customer_id, balance) VALUES (%s, %s)", (self.customer_id, self.credit_card_balance))
        engine.execute("INSERT INTO payments (customer_id, status) VALUES (%s, 'Late')", self.customer_id)
        engine.execute("INSERT INTO payments (customer_id, status) VALUES (%s, 'Late')", self.customer_id)

    def test_calculate_credit_score(self):
        calculate_credit_score(self.customer_id)
        result = engine.execute("SELECT credit_score FROM customers WHERE id = %s", self.customer_id).fetchone()
        self.assertIsNotNone(result)
        self.assertGreaterEqual(float(result[0]), 300)
        self.assertLessEqual(float(result[0]), 850)

    def test_calculate_credit_score_no_loans(self):
        engine.execute("DELETE FROM loans WHERE customer_id = %s", self.customer_id)
        calculate_credit_score(self.customer_id)
        result = engine.execute("SELECT credit_score FROM customers WHERE id = %s", self.customer_id).fetchone()
        self.assertIsNotNone(result)
        self.assertEqual(float(result[0]), 700)

    def test_calculate_credit_score_zero_balances(self):
        engine.execute("UPDATE loans SET loan_amount = 0 WHERE customer_id = %s", self.customer_id)
        engine.execute("UPDATE credit_cards SET balance = 0 WHERE customer_id = %s", self.customer_id)
        calculate_credit_score(self.customer_id)
        result = engine.execute("SELECT credit_score FROM customers WHERE id = %s", self.customer_id).fetchone()
        self.assertIsNotNone(result)
        self.assertEqual(float(result[0]), 700)

    def test_calculate_credit_score_low_score(self):
        engine.execute("UPDATE credits SET credit_score = 2000 WHERE id = %s", self.customer_id)
        calculate_credit_score(self.customer_id)
        result = engine.execute("SELECT credit_score FROM customers WHERE id = %s", self.customer_id).fetchone()
        self.assertIsNotNone(result)
        self.assertEqual(float(result[0]), 500)

    def tearDown(self):
        engine.execute("DELETE FROM loans WHERE customer_id = %s", self.customer_id)
        engine.execute("DELETE FROM credit_cards WHERE customer_id = %s", self.customer_id)
        engine.execute("DELETE FROM payments WHERE customer_id = %s", self.customer_id)
        engine.execute("DELETE FROM customers WHERE id = %s", self.customer_id)


if __name__ == '__main__':
    unittest.main()
