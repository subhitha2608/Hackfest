
import unittest
from unittest.mock import patch, Mock
from your_module import transfer_funds  # replace 'your_module' with the actual module name

class TestTransferFunds(unittest.TestCase):
    @patch('your_module.engine')
    def test_transfer_funds_success(self, mock_engine):
        p_sender = 1
        p_receiver = 2
        p_amount = 10

        mock_connect = mock_engine.connect.return_value
        mock_execute = mock_connect.execute
        mock_commit = mock_connect.commit

        transfer_funds(p_sender, p_receiver, p_amount)

        mock_engine.connect.assert_called_once()
        self.assertEqual(mock_execute.call_count, 2)
        mock_execute.assert_any_call(sa.text("UPDATE accounts SET balance = balance - :amount WHERE id = :sender;"), {'sender': p_sender, 'amount': p_amount})
        mock_execute.assert_any_call(sa.text("UPDATE accounts SET balance = :amount + balance WHERE id = :receiver;"), {'receiver': p_receiver, 'amount': p_amount})
        mock_commit.assert_called_once()

    @patch('your_module.engine')
    def test_transfer_funds_sender_receiver_same(self, mock_engine):
        p_sender = 1
        p_receiver = 1
        p_amount = 10

        mock_connect = mock_engine.connect.return_value
        mock_execute = mock_connect.execute
        mock_commit = mock_connect.commit

        with self.assertRaises(ValueError):
            transfer_funds(p_sender, p_receiver, p_amount)

    @patch('your_module.engine')
    def test_transfer_funds_amount_zero(self, mock_engine):
        p_sender = 1
        p_receiver = 2
        p_amount = 0

        mock_connect = mock_engine.connect.return_value
        mock_execute = mock_connect.execute
        mock_commit = mock_connect.commit

        with self.assertRaises(ValueError):
            transfer_funds(p_sender, p_receiver, p_amount)

    @patch('your_module.engine')
    def test_transfer_funds_amount_negative(self, mock_engine):
        p_sender = 1
        p_receiver = 2
        p_amount = -10

        mock_connect = mock_engine.connect.return_value
        mock_execute = mock_connect.execute
        mock_commit = mock_connect.commit

        with self.assertRaises(ValueError):
            transfer_funds(p_sender, p_receiver, p_amount)

if __name__ == '__main__':
    unittest.main()
