
import unittest
from your_module import transfer_amount
import pandas as pd
from sqlalchemy import text
from unittest.mock import patch

class TestTransferAmount(unittest.TestCase):

    @patch('your_module.engine.connect')
    def test_transfer_amount_success(self, connect):
        conn = connect.return_value
        conn.execute.return_value = None
        conn.commit.return_value = None
        conn.close.return_value = None

        result = transfer_amount(1, 2, 100)
        self.assertIsNone(result)
        conn.execute.assert_called_with(text("""
            UPDATE accounts
            SET balance = balance - :p_amount
            WHERE id = :p_sender
        """).bindparams(p_sender=1, p_amount=100))
        conn.execute.assert_called_with(text("""
            UPDATE accounts
            SET balance = balance + :p_amount
            WHERE id = :p_receiver
        """).bindparams(p_receiver=2, p_amount=100))
        conn.commit.assert_called_once()
        conn.close.assert_called_once()

    @patch('your_module.engine.connect')
    def test_transfer_amount_sender_account_exists(self, connect):
        conn = connect.return_value
        conn.execute.return_value = None
        conn.commit.return_value = None
        conn.close.return_value = None

        result = transfer_amount(1, 2, 100)
        self.assertIsNone(result)
        conn.execute.assert_called_with(text("""
            UPDATE accounts
            SET balance = balance - :p_amount
            WHERE id = :p_sender
        """).bindparams(p_sender=1, p_amount=100))
        conn.execute.assert_called_with(text("""
            UPDATE accounts
            SET balance = balance + :p_amount
            WHERE id = :p_receiver
        """).bindparams(p_receiver=2, p_amount=100))
        conn.commit.assert_called_once()
        conn.close.assert_called_once()

    @patch('your_module.engine.connect')
    def test_transfer_amount_receiver_account_exists(self, connect):
        conn = connect.return_value
        conn.execute.return_value = None
        conn.commit.return_value = None
        conn.close.return_value = None

        result = transfer_amount(1, 2, 100)
        self.assertIsNone(result)
        conn.execute.assert_called_with(text("""
            UPDATE accounts
            SET balance = balance - :p_amount
            WHERE id = :p_sender
        """).bindparams(p_sender=1, p_amount=100))
        conn.execute.assert_called_with(text("""
            UPDATE accounts
            SET balance = balance + :p_amount
            WHERE id = :p_receiver
        """).bindparams(p_receiver=2, p_amount=100))
        conn.commit.assert_called_once()
        conn.close.assert_called_once()

    @patch('your_module.engine.connect')
    def test_transfer_amount_zero_amount(self, connect):
        conn = connect.return_value
        conn.execute.return_value = None
        conn.commit.return_value = None
        conn.close.return_value = None

        result = transfer_amount(1, 2, 0)
        self.assertIsNone(result)
        conn.execute.assert_not_called()
        conn.commit.assert_not_called()
        conn.close.assert_called_once()

    @patch('your_module.engine.connect')
    def test_transfer_amount_invalid_sender_account(self, connect):
        conn = connect.return_value
        conn.execute.side_effect = [None, None, Exception('Invalid sender ID')]
        conn.commit.return_value = None
        conn.close.return_value = None

        with self.assertRaises(Exception):
            transfer_amount(99, 2, 100)

    @patch('your_module.engine.connect')
    def test_transfer_amount_invalid_receiver_account(self, connect):
        conn = connect.return_value
        conn.execute.side_effect = [None, Exception('Invalid receiver ID'), None]
        conn.commit.return_value = None
        conn.close.return_value = None

        with self.assertRaises(Exception):
            transfer_amount(1, 99, 100)

    @patch('your_module.engine.connect')
    def test_transfer_amount_error_occurred(self, connect):
        conn = connect.return_value
        conn.execute.side_effect = Exception('Error occurred')
        conn.commit.return_value = None
        conn.close.return_value = None

        with self.assertRaises(Exception):
            transfer_amount(1, 2, 100)

if __name__ == '__main__':
    unittest.main()
