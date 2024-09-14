
import unittest
from your_module import transfer_funds  # replace with the actual module name

class TestTransferFunds(unittest.TestCase):
    def setUp(self):
        # Create a test database connection
        self.conn = engine.connect()

        # Create test accounts with initial balances
        self.sender_id = 1
        self.receiver_id = 2
        self.initial_balance = 100
        self.conn.execute(text("INSERT INTO accounts (id, balance) VALUES (:id, :balance)"),
                           [{'id': self.sender_id, 'balance': self.initial_balance},
                            {'id': self.receiver_id, 'balance': self.initial_balance}])
        self.conn.commit()

    def tearDown(self):
        # Rollback any changes made during the test
        self.conn.rollback()
        self.conn.close()

    def test_transfer_funds_positive(self):
        # Positive test: transfer funds from sender to receiver
        p_amount = 50
        transfer_funds(self.sender_id, self.receiver_id, p_amount)

        # Verify that the balances have been updated correctly
        sender_balance = self.conn.execute(text("SELECT balance FROM accounts WHERE id = :id"), {'id': self.sender_id}).fetchone()[0]
        receiver_balance = self.conn.execute(text("SELECT balance FROM accounts WHERE id = :id"), {'id': self.receiver_id}).fetchone()[0]
        self.assertEqual(sender_balance, self.initial_balance - p_amount)
        self.assertEqual(receiver_balance, self.initial_balance + p_amount)

    def test_transfer_funds_zero_amount(self):
        # Test transferring zero amount
        p_amount = 0
        transfer_funds(self.sender_id, self.receiver_id, p_amount)

        # Verify that the balances remain unchanged
        sender_balance = self.conn.execute(text("SELECT balance FROM accounts WHERE id = :id"), {'id': self.sender_id}).fetchone()[0]
        receiver_balance = self.conn.execute(text("SELECT balance FROM accounts WHERE id = :id"), {'id': self.receiver_id}).fetchone()[0]
        self.assertEqual(sender_balance, self.initial_balance)
        self.assertEqual(receiver_balance, self.initial_balance)

    def test_transfer_funds_negative_amount(self):
        # Test transferring negative amount
        p_amount = -50
        with self.assertRaises(ValueError):
            transfer_funds(self.sender_id, self.receiver_id, p_amount)

    def test_transfer_funds_invalid_sender_id(self):
        # Test transferring funds with invalid sender ID
        p_amount = 50
        with self.assertRaises(sqlalchemy.exc.NoSuchTable):
            transfer_funds(999, self.receiver_id, p_amount)

    def test_transfer_funds_invalid_receiver_id(self):
        # Test transferring funds with invalid receiver ID
        p_amount = 50
        with self.assertRaises(sqlalchemy.exc.NoSuchTable):
            transfer_funds(self.sender_id, 999, p_amount)

if __name__ == '__main__':
    unittest.main()
