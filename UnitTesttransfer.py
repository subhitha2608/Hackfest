
import unittest
from your_module import transfer_funds
from your_module import engine

class TestTransferFunds(unittest.TestCase):

    def setUp(self):
        # Create test data
        self.sender_id = 1
        self.receiver_id = 2
        self.amount = 100
        self.new_balance_sender = 900
        self.new_balance_receiver = 1000

        # Create test db rows
        df = pd.DataFrame({'id': [self.sender_id, self.receiver_id], 'balance': [1000, 0]})
        df.to_sql('accounts', engine, if_exists='replace', index=False)

    def test_transfer_funds(self):
        transfer_funds(self.sender_id, self.receiver_id, self.amount)
        sender_result = engine.execute('SELECT balance FROM accounts WHERE id = :id', {'id': self.sender_id}).fetchone()[0]
        receiver_result = engine.execute('SELECT balance FROM accounts WHERE id = :id', {'id': self.receiver_id}).fetchone()[0]
        self.assertEqual(sender_result, self.new_balance_sender)
        self.assertEqual(receiver_result, self.new_balance_receiver)

    def test_transfer_zero_amount(self):
        transfer_funds(self.sender_id, self.receiver_id, 0)
        sender_result = engine.execute('SELECT balance FROM accounts WHERE id = :id', {'id': self.sender_id}).fetchone()[0]
        receiver_result = engine.execute('SELECT balance FROM accounts WHERE id = :id', {'id': self.receiver_id}).fetchone()[0]
        self.assertEqual(sender_result, 1000)
        self.assertEqual(receiver_result, 0)

    def test_transfer_negative_amount(self):
        with self.assertRaises(ValueError):
            transfer_funds(self.sender_id, self.receiver_id, -100)

    def test_transfer_funds_invalid_sender_id(self):
        with self.assertRaises(ValueError):
            transfer_funds(-1, self.receiver_id, self.amount)

    def test_transfer_funds_invalid_receiver_id(self):
        with self.assertRaises(ValueError):
            transfer_funds(self.sender_id, -1, self.amount)

    def tearDown(self):
        # Drop test db
        engine.execute('DROP TABLE accounts;')

if __name__ == '__main__':
    unittest.main()
