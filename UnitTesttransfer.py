
import unittest
from your_module import transfer_amount  # Import the function to be tested
import pandas as pd
from sqlalchemy import create_engine

class TestTransferAmount(unittest.TestCase):
    def setUp(self):
        # Create a test database connection
        self.engine = create_engine('postgresql://user:password@host:port/dbname')
        self.conn = self.engine.connect()

        # Create a test table with some sample data
        self.conn.execute("""
            CREATE TABLE accounts (
                id SERIAL PRIMARY KEY,
                balance INTEGER
            );
        """)

        self.conn.execute("""
            INSERT INTO accounts (balance) VALUES (100);
        """)
        self.conn.execute("""
            INSERT INTO accounts (balance) VALUES (50);
        """)

    def tearDown(self):
        # Drop the test table and close the connection
        self.conn.execute("DROP TABLE accounts;")
        self.conn.close()

    def test_transfer_amount_positive(self):
        # Test a successful transfer
        sender_id = 1
        receiver_id = 2
        amount = 20
        initial_sender_balance = 100
        initial_receiver_balance = 50

        transfer_amount(sender_id, receiver_id, amount)

        # Check the updated balances
        result = self.conn.execute("SELECT balance FROM accounts WHERE id = 1;")
        self.assertEqual(result.fetchone()[0], initial_sender_balance - amount)
        result = self.conn.execute("SELECT balance FROM accounts WHERE id = 2;")
        self.assertEqual(result.fetchone()[0], initial_receiver_balance + amount)

    def test_transfer_amount_insufficient_funds(self):
        # Test a transfer with insufficient funds
        sender_id = 1
        receiver_id = 2
        amount = 150  # More than the sender's balance
        initial_sender_balance = 100
        initial_receiver_balance = 50

        with self.assertRaises(psycopg2.Error):
            transfer_amount(sender_id, receiver_id, amount)

        # Check that the balances are unchanged
        result = self.conn.execute("SELECT balance FROM accounts WHERE id = 1;")
        self.assertEqual(result.fetchone()[0], initial_sender_balance)
        result = self.conn.execute("SELECT balance FROM accounts WHERE id = 2;")
        self.assertEqual(result.fetchone()[0], initial_receiver_balance)

    def test_transfer_amount_invalid_sender(self):
        # Test a transfer with an invalid sender ID
        sender_id = 3  # Does not exist
        receiver_id = 2
        amount = 20

        with self.assertRaises(psycopg2.Error):
            transfer_amount(sender_id, receiver_id, amount)

    def test_transfer_amount_invalid_receiver(self):
        # Test a transfer with an invalid receiver ID
        sender_id = 1
        receiver_id = 3  # Does not exist
        amount = 20

        with self.assertRaises(psycopg2.Error):
            transfer_amount(sender_id, receiver_id, amount)

    def test_transfer_amount_zero_amount(self):
        # Test a transfer with a zero amount
        sender_id = 1
        receiver_id = 2
        amount = 0

        transfer_amount(sender_id, receiver_id, amount)

        # Check that the balances are unchanged
        result = self.conn.execute("SELECT balance FROM accounts WHERE id = 1;")
        self.assertEqual(result.fetchone()[0], 100)
        result = self.conn.execute("SELECT balance FROM accounts WHERE id = 2;")
        self.assertEqual(result.fetchone()[0], 50)

    def test_transfer_amount_negative_amount(self):
        # Test a transfer with a negative amount
        sender_id = 1
        receiver_id = 2
        amount = -20

        with self.assertRaises(psycopg2.Error):
            transfer_amount(sender_id, receiver_id, amount)

if __name__ == '__main__':
    unittest.main()
