
import unittest
from your_module import calculate_credit_score  # Replace with the actual module name

class TestCalculateCreditScore(unittest.TestCase):
    def test_calculate_credit_score_happy_path(self):
        customer_id = 123  # Replace with a valid customer ID
        credit_score = calculate_credit_score(customer_id)
        self.assertEquals(credit_score, 650)  # Replace with the expected credit score

    def test_calculate_credit_score_no_loans(self):
        customer_id = 456  # Replace with a customer ID with no loans
        credit_score = calculate_credit_score(customer_id)
        self.assertEquals(credit_score, 700)  # Replace with the expected credit score

    def test_calculate_credit_score_late_payments(self):
        customer_id = 789  # Replace with a customer ID with late payments
        credit_score = calculate_credit_score(customer_id)
        self.assertEquals(credit_score, 400)  # Replace with the expected credit score

if __name__ == '__main__':
    unittest.main()
