
import unittest
from calculate_credit_score import calculate_credit_score

class TestCalculateCreditScore(unittest.TestCase):
    def test_calculate_credit_score customerId1(self):
        customer_id = 1
        result = calculate_credit_score(customer_id)
        self.assertEquals(result, 650)  # Replace with expected result for customer_id 1

    def test_calculate_credit_score_customerId2(self):
        customer_id = 2
        result = calculate_credit_score(customer_id)
        self.assertEquals(result, 700)  # Replace with expected result for customer_id 2

    def test_calculate_credit_score_customerId3(self):
        customer_id = 3
        result = calculate_credit_score(customer_id)
        self.assertEquals(result, 550)  # Replace with expected result for customer_id 3

if __name__ == '__main__':
    unittest.main()
