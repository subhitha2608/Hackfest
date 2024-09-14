
import unittest
from your_module import calculate_credit_score  # Replace with the actual module name

class TestCalculateCreditScore(unittest.TestCase):
    def test_calculate_credit_score(self):
        # Test with a customer who has loans, credit cards, and late payments
        customer_id = 1
        credit_score = calculate_credit_score(customer_id)
        self.assertEqual(credit_score, 650)

    def test_calculate_credit_score_no_loans(self):
        # Test with a customer who has no loans
        customer_id = 2
        credit_score = calculate_credit_score(customer_id)
        self.assertEqual(credit_score, 700)

    def test_calculate_credit_score_no_credit_cards(self):
        # Test with a customer who has no credit cards
        customer_id = 3
        credit_score = calculate_credit_score(customer_id)
        self.assertEqual(credit_score, 750)

if __name__ == '__main__':
    unittest.main()
