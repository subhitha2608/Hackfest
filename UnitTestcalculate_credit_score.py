
import unittest
from your_module import calculate_credit_score  # Replace 'your_module' with the actual module name

class TestCalculateCreditScore(unittest.TestCase):

    def test_calculate_credit_score_positive(self):
        # Test with existing customer and loans
        customer_id = 1
        expected_credit_score = 750
        self.assertEqual(calculate_credit_score(customer_id), expected_credit_score)

    def test_calculate_credit_score_non_existent_customer(self):
        # Test with non-existent customer
        customer_id = 1000
        with self.assertRaises(psycopg2.Error):
            calculate_credit_score(customer_id)

    def test_calculate_credit_score_no_loans(self):
        # Test with existing customer but no loans
        customer_id = 2
        expected_credit_score = 700
        self.assertEqual(calculate_credit_score(customer_id), expected_credit_score)

    def test_calculate_credit_score_late_payments(self):
        # Test with existing customer, loans and late payments
        customer_id = 3
        expected_credit_score = 550
        self.assertEqual(calculate_credit_score(customer_id), expected_credit_score)

    def test_calculate_credit_score_high_credit_card_balance(self):
        # Test with existing customer, loans and high credit card balance
        customer_id = 4
        expected_credit_score = 400
        self.assertEqual(calculate_credit_score(customer_id), expected_credit_score)

    def test_calculate_credit_score_low_credit_score(self):
        # Test with existing customer, loans and low credit score
        customer_id = 5
        expected_credit_score = 300
        self.assertEqual(calculate_credit_score(customer_id), expected_credit_score)

    def test_calculate_credit_score_log_alert(self):
        # Test with existing customer, loans and low credit score (logging alert)
        customer_id = 6
        expected_credit_score = 400
        self.assertEqual(calculate_credit_score(customer_id), expected_credit_score)

if __name__ == '__main__':
    unittest.main()
