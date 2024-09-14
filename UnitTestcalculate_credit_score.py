
import unittest
from your_module import calculate_credit_score  # Replace 'your_module' with the actual module name

class TestCalculateCreditScore(unittest.TestCase):
    def setUp(self):
        # Establish a test database connection
        self.conn = engine.connect()

    def tearDown(self):
        # Close the test database connection
        self.conn.close()

    def test_calculate_credit_score_valid_customer_id(self):
        # Test with a valid customer ID
        customer_id = 1
        credit_score = calculate_credit_score(customer_id)
        self.assertIsInstance(credit_score, (int, float))
        self.assertGreaterEqual(credit_score, 300)
        self.assertLessEqual(credit_score, 850)

    def test_calculate_credit_score_invalid_customer_id(self):
        # Test with an invalid customer ID
        customer_id = -1
        with self.assertRaises(Exception):
            calculate_credit_score(customer_id)

    def test_calculate_credit_score_no_loans(self):
        # Test with a customer who has no loans
        customer_id = 2
        credit_score = calculate_credit_score(customer_id)
        self.assertEqual(credit_score, 400)  # default score for no loans

    def test_calculate_credit_score_zero_credit_card_balance(self):
        # Test with a customer who has a zero credit card balance
        customer_id = 3
        credit_score = calculate_credit_score(customer_id)
        self.assertEqual(credit_score, 700)  # default score for zero credit card balance

    def test_calculate_credit_score_multiple_late_payments(self):
        # Test with a customer who has multiple late payments
        customer_id = 4
        credit_score = calculate_credit_score(customer_id)
        self.assertLess(credit_score, 400)  # score should be decreased due to late payments

    def test_calculate_credit_score_low_credit_score_alert(self):
        # Test with a customer who has a low credit score
        customer_id = 5
        credit_score = calculate_credit_score(customer_id)
        self.assertLess(credit_score, 500)
        # Check if an alert was inserted into the database
        query = "SELECT * FROM credit_score_alerts WHERE customer_id = :customer_id"
        result = self.conn.execute(query, {'customer_id': customer_id})
        self.assertIsNotNone(result.fetchone())

if __name__ == '__main__':
    unittest.main()
