
import unittest
from your_module import calculate_credit_score  # Replace with the actual module name

class TestCalculateCreditScore(unittest.TestCase):
    def test_customer_with_loans_and_credit_card(self):
        customer_id = 1  # Assuming customer with ID 1 has loans and credit card
        credit_score = calculate_credit_score(customer_id)
        self.assertEquals(credit_score, 650)  # Replace with the expected credit score for this customer

    def test_customer_with_only_loans(self):
        customer_id = 2  # Assuming customer with ID 2 has only loans
        credit_score = calculate_credit_score(customer_id)
        self.assertEquals(credit_score, 700)  # Replace with the expected credit score for this customer

    def test_customer_with_no_credit_history(self):
        customer_id = 3  # Assuming customer with ID 3 has no credit history
        credit_score = calculate_credit_score(customer_id)
        self.assertEquals(credit_score, 500)  # Replace with the expected credit score for this customer

if __name__ == '__main__':
    unittest.main()
