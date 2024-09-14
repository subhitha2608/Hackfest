
import unittest
from your_module import calculate_credit_score  # Import the function to be tested

class TestCalculateCreditScore(unittest.TestCase):
    def setUp(self):
        # Set up a test database connection
        self.engine = engine  # Assuming engine is defined in the same module
        self.conn = self.engine.connect()
        self.conn.execute("CREATE TABLE loans (customer_id integer, loan_amount numeric, repayment_amount numeric, outstanding_balance numeric)")
        self.conn.execute("CREATE TABLE credit_cards (customer_id integer, balance numeric)")
        self.conn.execute("CREATE TABLE payments (customer_id integer, status text)")
        self.conn.execute("CREATE TABLE customers (id integer, credit_score numeric)")
        self.conn.execute("CREATE TABLE credit_score_alerts (customer_id integer, credit_score numeric, created_at timestamp)")

    def tearDown(self):
        # Clean up the test database
        self.conn.execute("DROP TABLE loans")
        self.conn.execute("DROP TABLE credit_cards")
        self.conn.execute("DROP TABLE payments")
        self.conn.execute("DROP TABLE customers")
        self.conn.execute("DROP TABLE credit_score_alerts")
        self.conn.close()

    def test_calculate_credit_score_positive(self):
        # Insert test data
        self.conn.execute("INSERT INTO loans (customer_id, loan_amount, repayment_amount, outstanding_balance) VALUES (1, 1000, 500, 500)")
        self.conn.execute("INSERT INTO credit_cards (customer_id, balance) VALUES (1, 2000)")
        self.conn.execute("INSERT INTO payments (customer_id, status) VALUES (1, 'On Time')")
        self.conn.execute("INSERT INTO customers (id) VALUES (1)")

        # Call the function
        credit_score = calculate_credit_score(1)

        # Assert the result
        self.assertAlmostEqual(credit_score, 650.0)  # Example score

    def test_calculate_credit_score_zero_loan_amount(self):
        # Insert test data
        self.conn.execute("INSERT INTO loans (customer_id, loan_amount, repayment_amount, outstanding_balance) VALUES (1, 0, 0, 0)")
        self.conn.execute("INSERT INTO credit_cards (customer_id, balance) VALUES (1, 2000)")
        self.conn.execute("INSERT INTO payments (customer_id, status) VALUES (1, 'On Time')")
        self.conn.execute("INSERT INTO customers (id) VALUES (1)")

        # Call the function
        credit_score = calculate_credit_score(1)

        # Assert the result
        self.assertAlmostEqual(credit_score, 700.0)  # Example score

    def test_calculate_credit_score_zero_credit_card_balance(self):
        # Insert test data
        self.conn.execute("INSERT INTO loans (customer_id, loan_amount, repayment_amount, outstanding_balance) VALUES (1, 1000, 500, 500)")
        self.conn.execute("INSERT INTO credit_cards (customer_id, balance) VALUES (1, 0)")
        self.conn.execute("INSERT INTO payments (customer_id, status) VALUES (1, 'On Time')")
        self.conn.execute("INSERT INTO customers (id) VALUES (1)")

        # Call the function
        credit_score = calculate_credit_score(1)

        # Assert the result
        self.assertAlmostEqual(credit_score, 750.0)  # Example score

    def test_calculate_credit_score_late_payment(self):
        # Insert test data
        self.conn.execute("INSERT INTO loans (customer_id, loan_amount, repayment_amount, outstanding_balance) VALUES (1, 1000, 500, 500)")
        self.conn.execute("INSERT INTO credit_cards (customer_id, balance) VALUES (1, 2000)")
        self.conn.execute("INSERT INTO payments (customer_id, status) VALUES (1, 'Late')")
        self.conn.execute("INSERT INTO customers (id) VALUES (1)")

        # Call the function
        credit_score = calculate_credit_score(1)

        # Assert the result
        self.assertAlmostEqual(credit_score, 600.0)  # Example score

    def test_calculate_credit_score_low_score_alert(self):
        # Insert test data
        self.conn.execute("INSERT INTO loans (customer_id, loan_amount, repayment_amount, outstanding_balance) VALUES (1, 1000, 500, 500)")
        self.conn.execute("INSERT INTO credit_cards (customer_id, balance) VALUES (1, 4000)")
        self.conn.execute("INSERT INTO payments (customer_id, status) VALUES (1, 'Late')")
        self.conn.execute("INSERT INTO customers (id) VALUES (1)")

        # Call the function
        credit_score = calculate_credit_score(1)

        # Assert the result
        self.assertAlmostEqual(credit_score, 400.0)  # Example score
        self.conn.execute("SELECT * FROM credit_score_alerts")
        result = self.conn.fetchone()
        self.assertEqual(result[1], 400)  # Check alert is raised

    def test_calculate_credit_score_customer_id_not_found(self):
        # Try to calculate credit score for non-existent customer
        with self.assertRaises(psycopg2.Error):
            calculate_credit_score(999)

if __name__ == '__main__':
    unittest.main()
