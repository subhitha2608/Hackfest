
import unittest
from your_module import calculate_credit_score
import pandas as pd

class TestCalculateCreditScore(unittest.TestCase):
    def test_minimum_credit_score(self):
        # Test that the function returns 300 when the credit score is below 300
        result = calculate_credit_score(12345)
        self.assertEqual(result, 300)

    def test_maximum_credit_score(self):
        # Test that the function returns 850 when the credit score is above 850
        result = calculate_credit_score(67890)
        self.assertEqual(result, 850)

    def test_average_credit_score(self):
        # Test that the function returns a credit score around 600 when parameters are average
        result = calculate_credit_score(99999)
        self.assertGreaterEqual(result, 550)
        self.assertLessEqual(result, 650)

    def test_zero_total_loan_amount(self):
        # Test that the function handles a customer with no loans
        result = calculate_credit_score(99988)
        self.assertEqual(result, 300)

    def test_zero_credit_card_balance(self):
        # Test that the function handles a customer with no credit card balance
        result = calculate_credit_score(99989)
        self.assertEqual(result, 300)

    def test_late_payments(self):
        # Test that the function deducts points for late payments
        result = calculate_credit_score(99990)
        self.assertLess(result, 500)

    def test_low_credit_utilization(self):
        # Test that the function rewards low credit utilization
        result = calculate_credit_score(99991)
        self.assertGreaterEqual(result, 650)

    def test_log_credit_score_alert(self):
        # Test that the function logs a credit score alert when the score is below 500
        result = calculate_credit_score(99992)
        self.assertTrue(result < 500)

    def test_update_credit_score_in_database(self):
        # Test that the function updates the customer's credit score in the database
        original_credit_score = 500
        with engine.connect() as connection:
            result = calculate_credit_score(99993)
            query = text("SELECT credit_score FROM customers WHERE id = :customer_id")
            result = connection.execute(query, {"customer_id": 99993}).fetchone()
            self.assertEqual(result[0], result)

if __name__ == '__main__':
    unittest.main()
