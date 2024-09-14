
import unittest
from your_module import calculate_credit_score  # Replace with the actual module name

class TestCalculateCreditScore(unittest.TestCase):
    def setUp(self):
        # Create a test database connection and some sample data
        self.engine = create_engine('sqlite:///:memory:')  # In-memory SQLite database
        self.conn = self.engine.connect()
        self.create_tables()
        self.insert_sample_data()

    def create_tables(self):
        # Create the necessary tables
        self.conn.execute("""
            CREATE TABLE loans (
                id INTEGER PRIMARY KEY,
                customer_id INTEGER,
                loan_amount REAL,
                repayment_amount REAL,
                outstanding_balance REAL
            );
        """)
        self.conn.execute("""
            CREATE TABLE credit_cards (
                id INTEGER PRIMARY KEY,
                customer_id INTEGER,
                balance REAL
            );
        """)
        self.conn.execute("""
            CREATE TABLE payments (
                id INTEGER PRIMARY KEY,
                customer_id INTEGER,
                status TEXT
            );
        """)
        self.conn.execute("""
            CREATE TABLE customers (
                id INTEGER PRIMARY KEY,
                credit_score INTEGER
            );
        """)
        self.conn.execute("""
            CREATE TABLE credit_score_alerts (
                id INTEGER PRIMARY KEY,
                customer_id INTEGER,
                credit_score INTEGER,
                created_at TIMESTAMP
            );
        """)

    def insert_sample_data(self):
        # Insert some sample data
        self.conn.execute("""
            INSERT INTO customers (id) VALUES (1);
        """)
        self.conn.execute("""
            INSERT INTO loans (customer_id, loan_amount, repayment_amount, outstanding_balance)
            VALUES (1, 10000, 5000, 5000);
        """)
        self.conn.execute("""
            INSERT INTO credit_cards (customer_id, balance) VALUES (1, 500);
        """)
        self.conn.execute("""
            INSERT INTO payments (customer_id, status) VALUES (1, 'On Time');
        """)
        self.conn.commit()

    def test_calculate_credit_score_with_data(self):
        # Test with sample data
        customer_id = 1
        credit_score = calculate_credit_score(customer_id)
        self/assertEqual(credit_score, 720)  # Expected credit score based on the sample data

    def test_calculate_credit_score_with_no_loans(self):
        # Test with no loans
        customer_id = 2
        self.conn.execute("""
            INSERT INTO customers (id) VALUES (2);
        """)
        self.conn.commit()
        credit_score = calculate_credit_score(customer_id)
        self.assertEqual(credit_score, 700)  # Expected credit score with no loans

    def test_calculate_credit_score_with_no_credit_cards(self):
        # Test with no credit cards
        customer_id = 3
        self.conn.execute("""
            INSERT INTO customers (id) VALUES (3);
        """)
        self.conn.execute("""
            INSERT INTO loans (customer_id, loan_amount, repayment_amount, outstanding_balance)
            VALUES (3, 10000, 5000, 5000);
        """)
        self.conn.commit()
        credit_score = calculate_credit_score(customer_id)
        self.assertEqual(credit_score, 680)  # Expected credit score with no credit cards

    def test_calculate_credit_score_with_late_payments(self):
        # Test with late payments
        customer_id = 4
        self.conn.execute("""
            INSERT INTO customers (id) VALUES (4);
        """)
        self.conn.execute("""
            INSERT INTO loans (customer_id, loan_amount, repayment_amount, outstanding_balance)
            VALUES (4, 10000, 5000, 5000);
        """)
        self.conn.execute("""
            INSERT INTO payments (customer_id, status) VALUES (4, 'Late');
        """)
        self.conn.commit()
        credit_score = calculate_credit_score(customer_id)
        self.assertEqual(credit_score, 630)  # Expected credit score with late payments

    def test_calculate_credit_score_with_invalid_customer_id(self):
        # Test with an invalid customer ID
        customer_id = 5
        with self.assertRaises(Exception):
            calculate_credit_score(customer_id)

    def tearDown(self):
        # Clean up the test database
        self.conn.close()
        self.engine.dispose()

if __name__ == '__main__':
    unittest.main()
