
import unittest
from your_module import calculate_credit_score  # Import the function to be tested

class TestCalculateCreditScore(unittest.TestCase):
    def setUp(self):
        # Create a test database connection (e.g., using a test database or in-memory database)
        self.conn = engine.connect()

    def tearDown(self):
        # Close the database connection
        self.conn.close()

    def test_calculate_credit_score_positive(self):
        # Test case: customer has loans, credit cards, and no late payments
        customer_id = 1
        total_loan_amount = 10000.0
        total_repayment = 5000.0
        outstanding_loan_balance = 3000.0
        credit_card_balance = 2000.0
        late_pay_count = 0

        # Insert test data into the database
        self.conn.execute("INSERT INTO loans (customer_id, loan_amount, repayment_amount, outstanding_balance) VALUES (%s, %s, %s, %s)", (customer_id, total_loan_amount, total_repayment, outstanding_loan_balance))
        self.conn.execute("INSERT INTO credit_cards (customer_id, balance) VALUES (%s, %s)", (customer_id, credit_card_balance))
        self.conn.commit()

        # Calculate the credit score
        credit_score = calculate_credit_score(customer_id)

        # Assert the credit score is within a reasonable range
        self.assertGreaterEqual(credit_score, 300)
        self.assertLessEqual(credit_score, 850)

    def test_calculate_credit_score_negative_loans(self):
        # Test case: customer has no loans, credit cards, and no late payments
        customer_id = 2
        credit_card_balance = 2000.0
        late_pay_count = 0

        # Insert test data into the database
        self.conn.execute("INSERT INTO credit_cards (customer_id, balance) VALUES (%s, %s)", (customer_id, credit_card_balance))
        self.conn.commit()

        # Calculate the credit score
        credit_score = calculate_credit_score(customer_id)

        # Assert the credit score is within a reasonable range
        self.assertGreaterEqual(credit_score, 300)
        self.assertLessEqual(credit_score, 850)

    def test_calculate_credit_score_negative_credit_cards(self):
        # Test case: customer has loans, no credit cards, and no late payments
        customer_id = 3
        total_loan_amount = 10000.0
        total_repayment = 5000.0
        outstanding_loan_balance = 3000.0

        # Insert test data into the database
        self.conn.execute("INSERT INTO loans (customer_id, loan_amount, repayment_amount, outstanding_balance) VALUES (%s, %s, %s, %s)", (customer_id, total_loan_amount, total_repayment, outstanding_loan_balance))
        self.conn.commit()

        # Calculate the credit score
        credit_score = calculate_credit_score(customer_id)

        # Assert the credit score is within a reasonable range
        self.assertGreaterEqual(credit_score, 300)
        self.assertLessEqual(credit_score, 850)

    def test_calculate_credit_score_late_payments(self):
        # Test case: customer has loans, credit cards, and 2 late payments
        customer_id = 4
        total_loan_amount = 10000.0
        total_repayment = 5000.0
        outstanding_loan_balance = 3000.0
        credit_card_balance = 2000.0
        late_pay_count = 2

        # Insert test data into the database
        self.conn.execute("INSERT INTO loans (customer_id, loan_amount, repayment_amount, outstanding_balance) VALUES (%s, %s, %s, %s)", (customer_id, total_loan_amount, total_repayment, outstanding_loan_balance))
        self.conn.execute("INSERT INTO credit_cards (customer_id, balance) VALUES (%s, %s)", (customer_id, credit_card_balance))
        self.conn.execute("INSERT INTO payments (customer_id, status) VALUES (%s, 'Late')", (customer_id,))
        self.conn.execute("INSERT INTO payments (customer_id, status) VALUES (%s, 'Late')", (customer_id,))
        self.conn.commit()

        # Calculate the credit score
        credit_score = calculate_credit_score(customer_id)

        # Assert the credit score is within a reasonable range
        self.assertGreaterEqual(credit_score, 300)
        self.assertLessEqual(credit_score, 850)

    def test_calculate_credit_score_non_existent_customer(self):
        # Test case: customer does not exist in the database
        customer_id = 999

        # Calculate the credit score
        with self.assertRaises(psycopg2.Error):
            calculate_credit_score(customer_id)

if __name__ == '__main__':
    unittest.main()
