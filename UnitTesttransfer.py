
import unittest
from unittest.mock import patch
from your_module import transfer_funds  # Replace with the actual module name

class TestTransferFunds(unittest.TestCase):
    def setUp(self):
        self.conn_patch = patch('your_module.engine.connect')
        self.conn_mock = self.conn_patch.start()
        self.conn_mock.return_value = self.conn_mock
        self.conn_mock.execute = mock.MagicMock()
        self.conn_mock.commit = mock.MagicMock()
        self.conn_mock.rollback = mock.MagicMock()
        self.conn_mock.close = mock.MagicMock()

    def tearDown(self):
        self.conn_patch.stop()

    def test_transfer_funds_success(self):
        # Test successful transfer
        p_sender = 1
        p_receiver = 2
        p_amount = 100
        transfer_funds(p_sender, p_receiver, p_amount)
        self.conn_mock.execute.assert_any_call(text("UPDATE accounts SET balance = balance - :amount WHERE id = :sender"), {'amount': p_amount, 'sender': p_sender})
        self.conn_mock.execute.assert_any_call(text("UPDATE accounts SET balance = balance + :amount WHERE id = :receiver"), {'amount': p_amount, 'receiver': p_receiver})
        self.conn_mock.commit.assert_called_once()
        self.conn_mock.close.assert_called_once()

    def test_transfer_funds_invalid_sender(self):
        # Test invalid sender ID
        p_sender = 999  # Non-existent ID
        p_receiver = 2
        p_amount = 100
        with self.assertRaises(psycopg2.Error):
            transfer_funds(p_sender, p_receiver, p_amount)
        self.conn_mock.rollback.assert_called_once()
        self.conn_mock.close.assert_called_once()

    def test_transfer_funds_invalid_receiver(self):
        # Test invalid receiver ID
        p_sender = 1
        p_receiver = 999  # Non-existent ID
        p_amount = 100
        with self.assertRaises(psycopg2.Error):
            transfer_funds(p_sender, p_receiver, p_amount)
        self.conn_mock.rollback.assert_called_once()
        self.conn_mock.close.assert_called_once()

    def test_transfer_funds_insufficient_funds(self):
        # Test insufficient funds in sender's account
        p_sender = 1
        p_receiver = 2
        p_amount = 1000  # More than the sender's balance
        with self.assertRaises(psycopg2.Error):
            transfer_funds(p_sender, p_receiver, p_amount)
        self.conn_mock.rollback.assert_called_once()
        self.conn_mock.close.assert_called_once()

    def test_transfer_funds_invalid_amount(self):
        # Test invalid amount (negative or zero)
        p_sender = 1
        p_receiver = 2
        p_amount = -100  # Negative amount
        with self.assertRaises(ValueError):
            transfer_funds(p_sender, p_receiver, p_amount)
        p_amount = 0  # Zero amount
        with self.assertRaises(ValueError):
            transfer_funds(p_sender, p_receiver, p_amount)
        self.conn_mock.execute.assert_not_called()
        self.conn_mock.commit.assert_not_called()
        self.conn_mock.rollback.assert_not_called()
        self.conn_mock.close.assert_called_once()

if __name__ == '__main__':
    unittest.main()
