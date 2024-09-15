
import unittest
from your_module import transfer_amount  # replace with the actual module name

class TestTransferAmount(unittest.TestCase):
    def setUp(self):
        self.conn = engine.connect()

    def tearDown(self):
        self.conn.close()

    def test_transfer_amount_success(self):
        initial_sender_balance = self.conn.execute("SELECT balance FROM accounts WHERE id = 1").scalar()
        initial_receiver_balance = self.conn.execute("SELECT balance FROM accounts WHERE id = 2").scalar()
        transfer_amount(1, 2, 10)
        updated_sender_balance = self.conn.execute("SELECT balance FROM accounts WHERE id = 1").scalar()
        updated_receiver_balance = self.conn.execute("SELECT balance FROM accounts WHERE id = 2").scalar()
        self.assertEquals(updated_sender_balance, initial_sender_balance - 10)
        self.assertEquals(updated_receiver_balance, initial_receiver_balance + 10)

    def test_transfer_amount_insufficient_funds(self):
        with self.assertRaises(Exception):
            transfer_amount(1, 2, 1000)  # assume sender's balance is less than 1000

    def test_transfer_amount_invalid_receiver(self):
        with self.assertRaises(Exception):
            transfer_amount(1, 999, 10)  # assume receiver with id 999 does not exist

if __name__ == '__main__':
    unittest.main()
