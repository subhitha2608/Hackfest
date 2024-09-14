
import unittest
from your_module import transfer_funds  # Replace with the actual module name

class TestTransferFunds(unittest.TestCase):
    def setUp(self):
        # Create a test database connection
        self.conn = engine.connect()

        # Create test accounts with initial balances
        self.sender_id = 1
        self.receiver_id = 2
        self.initial_balance = 1000
        self.conn.execute("INSERT INTO accounts (id, balance) VALUES (%s, %s)", (self.sender_id, self.initial_balance))
        self.conn.execute("INSERT INTO accounts (id, balance) VALUES (%s, %s)", (self.receiver_id, self.initial_balance))
        self.conn.commit()

    def tearDown(self):
        # Clean up test data
        self.conn.execute("DELETE FROM accounts WHERE id IN (%s, %s)", (self.sender_id, self.receiver_id))
        self.conn.commit()
        self.conn.close()

    def test_transfer_funds_success(self):
        # Test successful fund transfer
        p_sender = self.sender_id
        p_receiver = self.receiver_id
        p_amount = 500
        transfer_funds(p_sender, p_receiver, p_amount)

        # Verify balances
        result = self.conn.execute("SELECT balance FROM accounts WHERE id = %s", (p_sender,))
        sender_balance = result.fetchone()[0]
        self.assertEqual(sender_balance, self.initial_balance - p_amount)

        result = self.conn.execute("SELECT balance FROM accounts WHERE id = %s", (p_receiver,))
        receiver_balance = result.fetchone()[0]
        self.assertEqual(receiver_balance, self.initial_balance + p_amount)

    def test_transfer_funds_insufficient_funds(self):
        # Test fund transfer with insufficient funds
        p_sender = self.sender_id
        p_receiver = self.receiver_id
        p_amount = self.initial_balance + 1
        with self.assertRaises(psycopg2.Error):
            transfer_funds(p_sender, p_receiver, p_amount)

        # Verify balances remain unchanged
        result = self.conn.execute("SELECT balance FROM accounts WHERE id = %s", (p_sender,))
        sender_balance = result.fetchone()[0]
        self.assertEqual(sender_balance, self.initial_balance)

        result = self.conn.execute("SELECT balance FROM accounts WHERE id = %s", (p_receiver,))
        receiver_balance = result.fetchone()[0]
        self.assertEqual(receiver_balance, self.initial_balance)

    def test_transfer_funds_invalid_account(self):
        # Test fund transfer with invalid account
        p_sender = 999  # Non-existent account
        p_receiver = self.receiver_id
        p_amount = 500
        with self.assertRaises(psycopg2.Error):
            transfer_funds(p_sender, p_receiver, p_amount)

        # Verify balances remain unchanged
        result = self.conn.execute("SELECT balance FROM accounts WHERE id = %s", (p_receiver,))
        receiver_balance = result.fetchone()[0]
        self.assertEqual(receiver_balance, self.initial_balance)

if __name__ == '__main__':
    unittest.main()
