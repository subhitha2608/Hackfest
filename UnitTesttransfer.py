
import unittest
from your_module import transfer_funds
import pandas as pd

class TestTransferFunds(unittest.TestCase):
    def setUp(self):
        # Create a test database connection
        self.conn = engine.connect()

        # Create a test accounts table
        self.conn.execute("""
            CREATE TABLE accounts (
                id SERIAL PRIMARY KEY,
                balance DECIMAL(10, 2) NOT NULL DEFAULT 0.00
            );
        """)

        # Insert some test data
        self.conn.execute("""
            INSERT INTO accounts (id, balance) VALUES
                (1, 100.00),
                (2, 50.00);
        """)

        # Commit the changes
        self.conn.commit()

    def tearDown(self):
        # Drop the test accounts table
        self.conn.execute("DROP TABLE accounts;")
        self.conn.close()

    def test_transfer_funds_positive(self):
        # Test a successful transfer
        transfer_funds(1, 2, 20.00)
        result = self.conn.execute("SELECT balance FROM accounts WHERE id = 1;").fetchone()
        self.assertEqual(result[0], 80.00)
        result = self.conn.execute("SELECT balance FROM accounts WHERE id = 2;").fetchone()
        self.assertEqual(result[0], 70.00)

    def test_transfer_funds_negative_sender_balance(self):
        # Test a transfer with insufficient sender balance
        with self.assertRaises(psycopg2.Error):
            transfer_funds(1, 2, 150.00)
        result = self.conn.execute("SELECT balance FROM accounts WHERE id = 1;").fetchone()
        self.assertEqual(result[0], 100.00)
        result = self.conn.execute("SELECT balance FROM accounts WHERE id = 2;").fetchone()
        self.assertEqual(result[0], 50.00)

    def test_transfer_funds_non_existent_sender(self):
        # Test a transfer with a non-existent sender
        with self.assertRaises(psycopg2.Error):
            transfer_funds(3, 2, 20.00)
        result = self.conn.execute("SELECT balance FROM accounts WHERE id = 2;").fetchone()
        self.assertEqual(result[0], 50.00)

    def test_transfer_funds_non_existent_receiver(self):
        # Test a transfer with a non-existent receiver
        with self.assertRaises(psycopg2.Error):
            transfer_funds(1, 3, 20.00)
        result = self.conn.execute("SELECT balance FROM accounts WHERE id = 1;").fetchone()
        self.assertEqual(result[0], 100.00)

    def test_transfer_funds_zero_amount(self):
        # Test a transfer with a zero amount
        with self.assertRaises(psycopg2.Error):
            transfer_funds(1, 2, 0.00)
        result = self.conn.execute("SELECT balance FROM accounts WHERE id = 1;").fetchone()
        self.assertEqual(result[0], 100.00)
        result = self.conn.execute("SELECT balance FROM accounts WHERE id = 2;").fetchone()
        self.assertEqual(result[0], 50.00)

    def test_transfer_funds_negative_amount(self):
        # Test a transfer with a negative amount
        with self.assertRaises(psycopg2.Error):
            transfer_funds(1, 2, -20.00)
        result = self.conn.execute("SELECT balance FROM accounts WHERE id = 1;").fetchone()
        self.assertEqual(result[0], 100.00)
        result = self.conn.execute("SELECT balance FROM accounts WHERE id = 2;").fetchone()
        self.assertEqual(result[0], 50.00)

if __name__ == '__main__':
    unittest.main()
