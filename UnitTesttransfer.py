
import unittest
from transfer_balance import transfer_balance

class TestTransferBalance(unittest.TestCase):
    def test_transfer_balance(self):
        # Initial balances: sender has 100, receiver has 50
        sender_id = 1
        receiver_id = 2
        amount = 20

        # Perform the transfer
        balances = transfer_balance(sender_id, receiver_id, amount)

        # Check the updated balances
        self.assertEqual(balances, [80, 70])  # sender now has 80, receiver now has 70

    def test_insufficient_balance(self):
        # Initial balances: sender has 50, receiver has 50
        sender_id = 1
        receiver_id = 2
        amount = 60  # exceeds sender's balance

        # Perform the transfer (should raise an exception)
        with self.assertRaises(Exception):
            transfer_balance(sender_id, receiver_id, amount)

    def test_same_account(self):
        # Initial balances: account has 100
        account_id = 1
        amount = 20

        # Perform the transfer (should raise an exception)
        with self.assertRaises(Exception):
            transfer_balance(account_id, account_id, amount)

if __name__ == '__main__':
    unittest.main()
