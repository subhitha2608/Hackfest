
import unittest
from your_module import transfer_funds  # Import the function to be tested

class TestTransferFunds(unittest.TestCase):
    def setUp(self):
        # Create a test database connection
        self.conn = engine.connect()

    def tearDown(self):
        # Close the test database connection
        self.conn.close()

    def test_transfer_funds_success(self):
        # Test a successful transfer
        sender_id = 1
        receiver_id = 2
        amount = 10.0
        initial_sender_balance = 100.0
        initial_receiver_balance = 50.0

        # Set up initial account balances
        self.conn.execute(text("UPDATE accounts SET balance = :balance WHERE id = :id"), {'balance': initial_sender_balance, 'id': sender_id})
        self.conn.execute(text("UPDATE accounts SET balance = :balance WHERE id = :id"), {'balance': initial_receiver_balance, 'id': receiver_id})

        # Call the function to be tested
        result = transfer_funds(sender_id, receiver_id, amount)

        # Check the result
        self.assertEqual(result, "Funds transferred successfully")

        # Check the updated account balances
        sender_balance = self.conn.execute(text("SELECT balance FROM accounts WHERE id = :id"), {'id': sender_id}).fetchone()[0]
        receiver_balance = self.conn.execute(text("SELECT balance FROM accounts WHERE id = :id"), {'id': receiver_id}).fetchone()[0]
        self.assertEqual(sender_balance, initial_sender_balance - amount)
        self.assertEqual(receiver_balance, initial_receiver_balance + amount)

    def test_transfer_funds_insufficient_funds(self):
        # Test a transfer with insufficient funds
        sender_id = 1
        receiver_id = 2
        amount = 150.0
        initial_sender_balance = 100.0
        initial_receiver_balance = 50.0

        # Set up initial account balances
        self.conn.execute(text("UPDATE accounts SET balance = :balance WHERE id = :id"), {'balance': initial_sender_balance, 'id': sender_id})
        self.conn.execute(text("UPDATE accounts SET balance = :balance WHERE id = :id"), {'balance': initial_receiver_balance, 'id': receiver_id})

        # Call the function to be tested
        with self.assertRaises(psycopg2.Error):
            transfer_funds(sender_id, receiver_id, amount)

        # Check that the account balances remain unchanged
        sender_balance = self.conn.execute(text("SELECT balance FROM accounts WHERE id = :id"), {'id': sender_id}).fetchone()[0]
        receiver_balance = self.conn.execute(text("SELECT balance FROM accounts WHERE id = :id"), {'id': receiver_id}).fetchone()[0]
        self.assertEqual(sender_balance, initial_sender_balance)
        self.assertEqual(receiver_balance, initial_receiver_balance)

    def test_transfer_funds_invalid_sender(self):
        # Test a transfer with an invalid sender ID
        sender_id = 999
        receiver_id = 2
        amount = 10.0

        # Call the function to be tested
        with self.assertRaises(psycopg2.Error):
            transfer_funds(sender_id, receiver_id, amount)

    def test_transfer_funds_invalid_receiver(self):
        # Test a transfer with an invalid receiver ID
        sender_id = 1
        receiver_id = 999
        amount = 10.0

        # Call the function to be tested
        with self.assertRaises(psycopg2.Error):
            transfer_funds(sender_id, receiver_id, amount)

if __name__ == '__main__':
    unittest.main()
