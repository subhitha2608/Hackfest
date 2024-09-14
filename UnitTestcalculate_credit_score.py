
import unittest
from your_module import calculate_credit_score  # Replace with the actual module name

class TestCalculateCreditScore(unittest.TestCase):
    def setUp(self):
        # Create a test database connection
        self.engine = create_engine('postgresql://user:password@host:port/dbname')  # Replace with your test DB credentials
        self.conn = self.engine.connect()

    def tearDown(self):
        # Close the test database connection
        self.conn.close()

    def test_calculate_credit_score_no_loans(self):
        # Create a test customer with no loans
        customer_id = 1
        self.conn.execute("INSERT INTO customers (id) VALUES (%s)", (customer_id,))

        # Calculate credit score
        credit_score = calculate_credit_score(customer_id)

        # Assert the credit score is 700 (average score)
        self.assertEqual(credit_score, 700)

    def test_calculate_credit_score_with_loans(self):
        # Create a test customer with loans
        customer_id = 2
        self.conn.execute("INSERT INTO customers (id) VALUES (%s)", (customer_id,))
        self.conn.execute("INSERT INTO loans (customer_id, loan_amount, repayment_amount, outstanding_balance) VALUES (%s, %s, %s, %s)", (customer_id, 1000, 500, 500))
        self.conn.execute("INSERT INTO loans (customer_id, loan_amount, repayment_amount, outstanding_balance) VALUES (%s, %s, %s, %s)", (customer_id, 2000, 1000, 1000))

        # Calculate credit score
        credit_score = calculate_credit_score(customer_id)

        # Assert the credit score is higher than 700 (due to loan repayment)
        self.assertGreater(credit_score, 700)

    def test_calculate_credit_score_with_credit_card(self):
        # Create a test customer with a credit card
        customer_id = 3
        self.conn.execute("INSERT INTO customers (id) VALUES (%s)", (customer_id,))
        self.conn.execute("INSERT INTO credit_cards (customer_id, balance) VALUES (%s, %s)", (customer_id, 5000))

        # Calculate credit score
        credit_score = calculate_credit_score(customer_id)

        # Assert the credit score is lower than 700 (due to credit card utilization)
        self.assertLess(credit_score, 700)

    def test_calculate_credit_score_with_late_payments(self):
        # Create a test customer with late payments
        customer_id = 4
        self.conn.execute("INSERT INTO customers (id) VALUES (%s)", (customer_id,))
        self.conn.execute("INSERT INTO payments (customer_id, status) VALUES (%s, %s)", (customer_id, 'Late'))
        self.conn.execute("INSERT INTO payments (customer_id, status) VALUES (%s, %s)", (customer_id, 'Late'))

        # Calculate credit score
        credit_score = calculate_credit_score(customer_id)

        # Assert the credit score is lower than 700 (due to late payments)
        self.assertLess(credit_score, 700)

if __name__ == '__main__':
    unittest.main()
