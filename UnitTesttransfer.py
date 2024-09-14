
import unittest
from your_module import transfer_amount  # replace with the actual module name

class TestTransferAmount(unittest.TestCase):
    def setUp(self):
        # Create a test connection to the database
        self.conn = engine.connect()

    def tearDown(self):
        # Close the test connection
        self.conn.close()

    def test_transfer_amount_success(self):
        # Test a successful transfer
        sender_id = 1
        receiver_id = 2
        amount = 10.0

        # Check initial balances
        sender_balance_before = self.get_balance(sender_id)
        receiver_balance_before = self.get_balance(receiver_id)

        transfer_amount(sender_id, receiver_id, amount)

        # Check updated balances
        sender_balance_after = self.get_balance(sender_id)
        receiver_balance_after = self.get_balance(receiver_id)

        self.assertAlmostEqual(sender_balance_before - amount, sender_balance_after)
        self.assertAlmostEqual(receiver_balance_before + amount, receiver_balance_after)

    def test_transfer_amount_insufficient_funds(self):
        # Test a transfer with insufficient funds
        sender_id = 1
        receiver_id = 2
        amount = 1000.0  # assume sender's balance is less than this

        with self.assertRaises(Exception):
            transfer_amount(sender_id, receiver_id, amount)

    def get_balance(self, account_id):
        # Helper function to get the current balance of an account
        query = text("SELECT balance FROM accounts WHERE id = :account_id")
        result = self.conn.execute(query, {'account_id': account_id}).fetchone()
        return result[0]

if __name__ == '__main__':
    unittest.main()
