
import unittest

class TestCalculateCreditScore(unittest.TestCase):
    def testcalculate_credit_score(self):
        customer_id = 1  # Replace with an existing customer ID
        expected_credit_score = 750  # Replace with the expected credit score for this customer
        result = calculate_credit_score(customer_id)
        self.assertEquals(result, expected_credit_score)

    def test_no_loans(self):
        customer_id = 2  # Replace with a customer ID with no loans
        expected_credit_score = 700  # Replace with the expected credit score for this customer
        result = calculate_credit_score(customer_id)
        self.assertEquals(result, expected_credit_score)

    def test_late_payments(self):
        customer_id = 3  # Replace with a customer ID with late payments
        expected_credit_score = 550  # Replace with the expected credit score for this customer
        result = calculate_credit_score(customer_id)
        self.assertEquals(result, expected_credit_score)

    def test_credit_card_balance(self):
        customer_id = 4  # Replace with a customer ID with a high credit card balance
        expected_credit_score = 400  # Replace with the expected credit score for this customer
        result = calculate_credit_score(customer_id)
        self.assertEquals(result, expected_credit_score)

if __name__ == '__main__':
    unittest.main()
