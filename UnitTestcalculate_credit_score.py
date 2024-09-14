
import unittest
from your_module import calculate_credit_score  # Replace with the actual module name

class TestCalculateCreditScore(unittest.TestCase):
    def setUp(self):
        # Create a test database connection and tables
        self.conn = engine.connect()
        self.conn.execute("CREATE TABLE loans (customer_id INT, loan_amount DECIMAL, repayment_amount DECIMAL, outstanding_balance DECIMAL)")
        self.conn.execute("CREATE TABLE credit_cards (customer_id INT, balance DECIMAL)")
        self.conn.execute("CREATE TABLE payments (customer_id INT, status VARCHAR)")
        self.conn.execute("CREATE TABLE customers (id INT, credit_score INT)")
        self.conn.execute("CREATE TABLE credit_score_alerts (customer_id INT, credit_score INT, created_at TIMESTAMP)")

    def tearDown(self):
        # Drop the test tables and close the connection
        self.conn.execute("DROP TABLE loans")
        self.conn.execute("DROP TABLE credit_cards")
        self.conn.execute("DROP TABLE payments")
        self.conn.execute("DROP TABLE customers")
        self.conn.execute("DROP TABLE credit_score_alerts")
        self.conn.close()

    def test_calculate_credit_score_with_loans_and_credit_cards(self):
        # Insert test data
        self.conn.execute("INSERT INTO loans (customer_id, loan_amount, repayment_amount, outstanding_balance) VALUES (1, 1000, 500, 200)")
        self.conn.execute("INSERT INTO credit_cards (customer_id, balance) VALUES (1, 500)")
        self.conn.execute("INSERT INTO customers (id) VALUES (1)")

        # Calculate credit score
        credit_score = calculate_credit_score(1)

        # Assert the result
        self.assertAlmostEqual(credit_score, 640, places=0)

    def test_calculate_credit_score_with_no_loans(self):
        # Insert test data
        self.conn.execute("INSERT INTO credit_cards (customer_id, balance) VALUES (1, 500)")
        self.conn.execute("INSERT INTO customers (id) VALUES (1)")

        # Calculate credit score
        credit_score = calculate_credit_score(1)

        # Assert the result
        self.assertAlmostEqual(credit_score, 700, places=0)

    def test_calculate_credit_score_with_late_payments(self):
        # Insert test data
        self.conn.execute("INSERT INTO loans (customer_id, loan_amount, repayment_amount, outstanding_balance) VALUES (1, 1000, 500, 200)")
        self.conn.execute("INSERT INTO credit_cards (customer_id, balance) VALUES (1, 500)")
        self.conn.execute("INSERT INTO payments (customer_id, status) VALUES (1, 'Late')")
        self.conn.execute("INSERT INTO customers (id) VALUES (1)")

        # Calculate credit score
        credit_score = calculate_credit_score(1)

        # Assert the result
        self.assertAlmostEqual(credit_score, 590, places=0)

    def test_calculate_credit_score_with_low_credit_card_balance(self):
        # Insert test data
        self.conn.execute("INSERT INTO loans (customer_id, loan_amount, repayment_amount, outstanding_balance) VALUES (1, 1000, 500, 200)")
        self.conn.execute("INSERT INTO credit_cards (customer_id, balance) VALUES (1, 100)")
        self.conn.execute("INSERT INTO customers (id) VALUES (1)")

        # Calculate credit score
        credit_score = calculate_credit_score(1)

        # Assert the result
        self.assertAlmostEqual(credit_score, 740, places=0)

    def test_calculate_credit_score_with_no_credit_card(self):
        # Insert test data
        self.conn.execute("INSERT INTO loans (customer_id, loan_amount, repayment_amount, outstanding_balance) VALUES (1, 1000, 500, 200)")
        self.conn.execute("INSERT INTO customers (id) VALUES (1)")

        # Calculate credit score
        credit_score = calculate_credit_score(1)

        # Assert the result
        self.assertAlmostEqual(credit_score, 680, places=0)

    def test_calculate_credit_score_with_non_numeric_data(self):
        # Insert test data with non-numeric values
        self.conn.execute("INSERT INTO loans (customer_id, loan_amount, repayment_amount, outstanding_balance) VALUES (1, 'abc', 'def', 'ghi')")
        self.conn.execute("INSERT INTO credit_cards (customer_id, balance) VALUES (1, 'jkl')")
        self.conn.execute("INSERT INTO customers (id) VALUES (1)")

        # Calculate credit score
        with self.assertRaises(ValueError):
            calculate_credit_score(1)

    def test_calculate_credit_score_with_customer_id_not_found(self):
        # Insert no data
        self.conn.execute("INSERT INTO customers (id) VALUES (2)")

        # Calculate credit score
        with self.assertRaises(Exception):
            calculate_credit_score(1)

if __name__ == '__main__':
    unittest.main()
