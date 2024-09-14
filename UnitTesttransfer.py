
import unittest
from unittest.mock import patch, MagicMock
from your_module import transfer_amount

class TestTransferAmount(unittest.TestCase):

    @patch('your_module.engine')
    def test_transfer_amount_success(self, mock_engine):
        mock_conn = MagicMock()
        mock_engine.connect.return_value = mock_conn
        p_sender = 1
        p_receiver = 2
        p_amount = 10

        transfer_amount(p_sender, p_receiver, p_amount)

        mock_conn.execute.assert_any_call(text("UPDATE accounts SET balance = balance - :p_amount WHERE id = :p_sender"), {"p_amount": p_amount, "p_sender": p_sender})
        mock_conn.execute.assert_any_call(text("UPDATE accounts SET balance = balance + :p_amount WHERE id = :p_receiver"), {"p_amount": p_amount, "p_receiver": p_receiver})
        mock_conn.commit.assert_called_once()
        mock_conn.close.assert_called_once()

    @patch('your_module.engine')
    def test_transfer_amount_zero_amount(self, mock_engine):
        mock_conn = MagicMock()
        mock_engine.connect.return_value = mock_conn
        p_sender = 1
        p_receiver = 2
        p_amount = 0

        transfer_amount(p_sender, p_receiver, p_amount)

        mock_conn.execute.assert_not_called()
        mock_conn.commit.assert_not_called()
        mock_conn.close.assert_called_once()

    @patch('your_module.engine')
    def test_transfer_amount_negative_amount(self, mock_engine):
        mock_conn = MagicMock()
        mock_engine.connect.return_value = mock_conn
        p_sender = 1
        p_receiver = 2
        p_amount = -10

        with self.assertRaises(ValueError):
            transfer_amount(p_sender, p_receiver, p_amount)

        mock_conn.execute.assert_not_called()
        mock_conn.commit.assert_not_called()
        mock_conn.close.assert_called_once()

    @patch('your_module.engine')
    def test_transfer_amount_invalid_sender(self, mock_engine):
        mock_conn = MagicMock()
        mock_engine.connect.return_value = mock_conn
        p_sender = None
        p_receiver = 2
        p_amount = 10

        with self.assertRaises(TypeError):
            transfer_amount(p_sender, p_receiver, p_amount)

        mock_conn.execute.assert_not_called()
        mock_conn.commit.assert_not_called()
        mock_conn.close.assert_called_once()

    @patch('your_module.engine')
    def test_transfer_amount_invalid_receiver(self, mock_engine):
        mock_conn = MagicMock()
        mock_engine.connect.return_value = mock_conn
        p_sender = 1
        p_receiver = None
        p_amount = 10

        with self.assertRaises(TypeError):
            transfer_amount(p_sender, p_receiver, p_amount)

        mock_conn.execute.assert_not_called()
        mock_conn.commit.assert_not_called()
        mock_conn.close.assert_called_once()

if __name__ == '__main__':
    unittest.main()
