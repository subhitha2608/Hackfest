
import unittest
from your_file import update_customer_credit_score  # Replace 'your_file' with the actual filename

class TestUpdateCustomerCreditScore(unittest.TestCase):
    # Test 1: Happy path with a valid customer ID
    def test_update_customer_credit_score_valid(self):
        v_credit_score = update_customer_credit_score(1)
        self.assertGreaterEqual(v_credit_score, 300)
        self.assertLessEqual(v_credit_score, 850)

    # Test 2: Happy path with a customer ID and no loans
    def test_update_customer_credit_score_no_loans(self):
        v_credit_score = update_customer_credit_score(2)
        self.assertEqual(v_credit_score, 650)

    # Test 3: Happy path with a customer ID and low credit card balance
    def test_update_customer_credit_score_low_credit_card_balance(self):
        v_credit_score = update_customer_credit_score(3)
        self.assertEqual(v_credit_score, 700)

    # Test 4: Happy path with a customer ID and high late payment count
    def test_update_customer_credit_score_high_late_payment_count(self):
        v_credit_score = update_customer_credit_score(4)
        self.assertEqual(v_credit_score, 250)

    # Test 5: Test with a customer ID and all loans repaid
    def test_update_customer_credit_score_all_loans_repaid(self):
        v_credit_score = update_customer_credit_score(5)
        self.assertEqual(v_credit_score, 850)

    # Test 6: Test with a customer ID and a credit score below 500
    def test_update_customer_credit_score_low_credit_score(self):
        v_credit_score = update_customer_credit_score(6)
        self.assertLess(v_credit_score, 500)

    # Test 7: Test with an invalid customer ID (throwing an exception)
    def test_update_customer_credit_score_invalid(self):
        with self.assertRaises(psycopg2.Error):
            update_customer_credit_score(999)

if __name__ == '__main__':
    unittest.main()
