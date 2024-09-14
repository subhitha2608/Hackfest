
import unittest
from your_module import calculate_credit_score  # Import the function to be tested

class TestCalculateCreditScore(unittest.TestCase):
    def setUp(self):
        # Create a test database connection
        self.conn = engine.connect()

    def tearDown(self):
        # Close the test database connection
        self.conn.close()

    def test_calculate_credit_score_positive(self):
        # Test with valid customer ID and non-zero loan amounts
        customer_id = 1
        self.conn.execute(text("INSERT INTO loans (customer_id, loan_amount, repayment_amount, outstanding_balance) VALUES (:customer_id, 1000, 500, 500)", {'customer_id': customer_id}))
        self.conn.execute(text("INSERT INTO credit_cards (customer_id, balance) VALUES (:customer_id, 2000)", {'customer_id': customer_id}))
        self.conn.execute(text("INSERT INTO payments (customer_id, status) VALUES (:customer_id, 'On Time')", {'customer_id': customer_id}))
        credit_score = calculate_credit_score(customer_id)
        self.assertGreaterEqual(credit_score, 300)
        self.assertLessEqual(credit_score, 850)

    def test_calculate_credit_score_zero_loan_amount(self):
        # Test with valid customer ID and zero loan amount
        customer_id = 2
        self.conn.execute(text("INSERT INTO loans (customer_id, loan_amount, repayment_amount, outstanding_balance) VALUES (:customer_id, 0, 0, 0)", {'customer_id': customer_id}))
        self.conn.execute(text("INSERT INTO credit_cards (customer_id, balance) VALUES (:customer_id, 2000)", {'customer_id': customer_id}))
        self.conn.execute(text("INSERT INTO payments (customer_id, status) VALUES (:customer_id, 'On Time')", {'customer_id': customer_id}))
        credit_score = calculate_credit_score(customer_id)
        self.assertEqual(credit_score, 700)

    def test_calculate_credit_score_no_credit_card(self):
        # Test with valid customer ID and no credit card balance
        customer_id = 3
        self.conn.execute(text("INSERT INTO loans (customer_id, loan_amount, repayment_amount, outstanding_balance) VALUES (:customer_id, 1000, 500, 500)", {'customer_id': customer_id}))
        self.conn.execute(text("INSERT INTO payments (customer_id, status) VALUES (:customer_id, 'On Time')", {'customer_id': customer_id}))
        credit_score = calculate_credit_score(customer_id)
        self.assertGreaterEqual(credit_score, 300)
        self.assertLessEqual(credit_score, 850)

    def test_calculate_credit_score_late_payments(self):
        # Test with valid customer ID and late payments
        customer_id = 4
        self.conn.execute(text("INSERT INTO loans (customer_id, loan_amount, repayment_amount, outstanding_balance) VALUES (:customer_id, 1000, 500, 500)", {'customer_id': customer_id}))
        self.conn.execute(text("INSERT INTO credit_cards (customer_id, balance) VALUES (:customer_id, 2000)", {'customer_id': customer_id}))
        self.conn.execute(text("INSERT INTO payments (customer_id, status) VALUES (:customer_id, 'Late')", {'customer_id': customer_id}))
        credit_score = calculate_credit_score(customer_id)
        self.assertLessEqual(credit_score, 650)

    def test_calculate_credit_score_invalid_customer_id(self):
        # Test with invalid customer ID
        customer_id = -1
        with self.assertRaises(psycopg2.Error):
            calculate_credit_score(customer_id)

    def test_calculate_credit_score_no_data(self):
        # Test with valid customer ID but no data in loans, credit_cards, or payments tables
        customer_id = 5
        credit_score = calculate_credit_score(customer_id)
        self.assertEqual(credit_score, 600)

if __name__ == '__main__':
    unittest.main()
