
import unittest
from your_module import transfer_amount
import pandas as pd
import psycopg2

class TestTransferAmount(unittest.TestCase):
    def setUp(self):
        # Create a test database connection
        self.conn = psycopg2.connect(
            dbname="your_database",
            user="your_username",
            password="your_password",
            host="your_host",
            port="your_port"
        )
        self.cursor = self.conn.cursor()

        # Create a test table with some sample data
        self.cursor.execute("""
            CREATE TABLE accounts (
                id SERIAL PRIMARY KEY,
                balance DECIMAL(10, 2)
            );
        """)
        self.cursor.execute("""
            INSERT INTO accounts (id, balance) VALUES
                (1, 100.00),
                (2, 200.00),
                (3, 300.00);
        """)
        self.conn.commit()

    def tearDown(self):
        # Drop the test table
        self.cursor.execute("DROP TABLE accounts;")
        self.conn.commit()
        self.conn.close()

    def test_transfer_amount_success(self):
        # Test a successful transfer
        sender_id = 1
        receiver_id = 2
        amount = 50.00

        initial_sender_balance = self.get_balance(sender_id)
        initial_receiver_balance = self.get_balance(receiver_id)

        transfer_amount(sender_id, receiver_id, amount)

        final_sender_balance = self.get_balance(sender_id)
        final_receiver_balance = self.get_balance(receiver_id)

        self.assertEqual(final_sender_balance, initial_sender_balance - amount)
        self.assertEqual(final_receiver_balance, initial_receiver_balance + amount)

    def test_transfer_amount_insufficient_funds(self):
        # Test a transfer with insufficient funds
        sender_id = 1
        receiver_id = 2
        amount = 150.00  # more than the sender's balance

        with self.assertRaises(psycopg2.Error):
            transfer_amount(sender_id, receiver_id, amount)

    def test_transfer_amount_invalid_sender(self):
        # Test a transfer with an invalid sender ID
        sender_id = 999  # non-existent ID
        receiver_id = 2
        amount = 50.00

        with self.assertRaises(psycopg2.Error):
            transfer_amount(sender_id, receiver_id, amount)

    def test_transfer_amount_invalid_receiver(self):
        # Test a transfer with an invalid receiver ID
        sender_id = 1
        receiver_id = 999  # non-existent ID
        amount = 50.00

        with self.assertRaises(psycopg2.Error):
            transfer_amount(sender_id, receiver_id, amount)

    def get_balance(self, account_id):
        self.cursor.execute("SELECT balance FROM accounts WHERE id = %s", (account_id,))
        return self.cursor.fetchone()[0]

if __name__ == '__main__':
    unittest.main()
