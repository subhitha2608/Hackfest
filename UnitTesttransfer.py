
import unittest
from your_module import transfer_balance

class TestTransferBalance(unittest.TestCase):
    def setUp(self):
        # Create a test database connection
        self.conn = engine.connect()

    def tearDown(self):
        # Close the test database connection
        self.conn.close()

    def test_transfer_balance_positive(self):
        # Test a successful transfer
        sender_id = 1
        receiver_id = 2
        amount = 10
        initial_sender_balance = 100
        initial_receiver_balance = 50

        # Set up initial balances
        self.conn.execute("UPDATE accounts SET balance = :balance WHERE id = :id", {"balance": initial_sender_balance, "id": sender_id})
        self.conn.execute("UPDATE accounts SET balance = :balance WHERE id = :id", {"balance": initial_receiver_balance, "id": receiver_id})

        # Call the function
        new_balances = transfer_balance(sender_id, receiver_id, amount)

        # Check the new balances
        self.assertEqual(new_balances, [initial_sender_balance - amount, initial_receiver_balance + amount])

    def test_transfer_balance_insufficient_funds(self):
        # Test a transfer with insufficient funds
        sender_id = 1
        receiver_id = 2
        amount = 150
        initial_sender_balance = 100
        initial_receiver_balance = 50

        # Set up initial balances
        self.conn.execute("UPDATE accounts SET balance = :balance WHERE id = :id", {"balance": initial_sender_balance, "id": sender_id})
        self.conn.execute("UPDATE accounts SET balance = :balance WHERE id = :id", {"balance": initial_receiver_balance, "id": receiver_id})

        # Call the function
        with self.assertRaises(psycopg2.Error):
            transfer_balance(sender_id, receiver_id, amount)

    def test_transfer_balance_invalid_account(self):
        # Test a transfer with an invalid account
        sender_id = 1
        receiver_id = 999
        amount = 10
        initial_sender_balance = 100
        initial_receiver_balance = 50

        # Set up initial balances
        self.conn.execute("UPDATE accounts SET balance = :balance WHERE id = :id", {"balance": initial_sender_balance, "id": sender_id})

        # Call the function
        with self.assertRaises(psycopg2.Error):
            transfer_balance(sender_id, receiver_id, amount)

    def test_transfer_balance_negative_amount(self):
        # Test a transfer with a negative amount
        sender_id = 1
        receiver_id = 2
        amount = -10
        initial_sender_balance = 100
        initial_receiver_balance = 50

        # Set up initial balances
        self.conn.execute("UPDATE accounts SET balance = :balance WHERE id = :id", {"balance": initial_sender_balance, "id": sender_id})
        self.conn.execute("UPDATE accounts SET balance = :balance WHERE id = :id", {"balance": initial_receiver_balance, "id": receiver_id})

        # Call the function
        with self.assertRaises(psycopg2.Error):
            transfer_balance(sender_id, receiver_id, amount)

if __name__ == '__main__':
    unittest.main()
