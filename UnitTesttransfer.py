
import unittest
from unittest.mock import patch, MagicMock
from your_module import transfer_funds

class TestTransferFunds(unittest.TestCase):

    @patch('your_module.engine')
    def test_transfer_funds(self, mock_engine):
        mock_conn = MagicMock()
        mock_engine.connect.return_value = mock_conn

        p_sender = 1
        p_receiver = 2
        p_amount = 10

        transfer_funds(p_sender, p_receiver, p_amount)

        mock_conn.execute.assert_any_call(text("""
            UPDATE accounts
            SET balance = balance - :p_amount
            WHERE id = :p_sender
        """), {"p_sender": p_sender, "p_amount": p_amount})

        mock_conn.execute.assert_any_call(text("""
            UPDATE accounts
            SET balance = balance + :p_amount
            WHERE id = :p_receiver
        """), {"p_receiver": p_receiver, "p_amount": p_amount})

        mock_conn.commit.assert_called_once()

    @patch('your_module.engine')
    def test_transfer_funds_same_account(self, mock_engine):
        mock_conn = MagicMock()
        mock_engine.connect.return_value = mock_conn

        p_sender = 1
        p_receiver = 1
        p_amount = 10

        transfer_funds(p_sender, p_receiver, p_amount)

        mock_conn.execute.assert_any_call(text("""
            UPDATE accounts
            SET balance = balance - :p_amount
            WHERE id = :p_sender
        """), {"p_sender": p_sender, "p_amount": p_amount})

        mock_conn.execute.assert_any_call(text("""
            UPDATE accounts
            SET balance = balance + :p_amount
            WHERE id = :p_receiver
        """), {"p_receiver": p_receiver, "p_amount": p_amount})

        mock_conn.commit.assert_called_once()

    @patch('your_module.engine')
    def test_transfer_funds_zero_amount(self, mock_engine):
        mock_conn = MagicMock()
        mock_engine.connect.return_value = mock_conn

        p_sender = 1
        p_receiver = 2
        p_amount = 0

        transfer_funds(p_sender, p_receiver, p_amount)

        mock_conn.execute.assert_any_call(text("""
            UPDATE accounts
            SET balance = balance - :p_amount
            WHERE id = :p_sender
        """), {"p_sender": p_sender, "p_amount": p_amount})

        mock_conn.execute.assert_any_call(text("""
            UPDATE accounts
            SET balance = balance + :p_amount
            WHERE id = :p_receiver
        """), {"p_receiver": p_receiver, "p_amount": p_amount})

        mock_conn.commit.assert_called_once()

    @patch('your_module.engine')
    def test_transfer_funds_negative_amount(self, mock_engine):
        mock_conn = MagicMock()
        mock_engine.connect.return_value = mock_conn

        p_sender = 1
        p_receiver = 2
        p_amount = -10

        with self.assertRaises(ValueError):
            transfer_funds(p_sender, p_receiver, p_amount)

if __name__ == '__main__':
    unittest.main()
