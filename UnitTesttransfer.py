
import unittest
from your_module import transfer_amount  # Replace with the actual module name

class TestTransferAmount(unittest.TestCase):
    def test_transfer_amount_success(self):
        p_sender = 1
        p_receiver = 2
        p_amount = 10
        balances = transfer_amount(p_sender, p_receiver, p_amount)
        self.assertEquals(balances[0]['balance'], 90)  # Assuming sender's initial balance is 100
        self.assertEquals(balances[1]['balance'], 110)  # Assuming receiver's initial balance is 100

    def test_transfer_amount_insufficient_funds(self):
        p_sender = 1
        p_receiver = 2
        p_amount = 150  # More than sender's balance
        with self.assertRaises(psycopg2.Error):
            transfer_amount(p_sender, p_receiver, p_amount)

    def test_transfer_amount_invalid_account(self):
        p_sender = 1
        p_receiver = 999  # Non-existent account
        p_amount = 10
        with self.assertRaises(psycopg2.Error):
            transfer_amount(p_sender, p_receiver, p_amount)
