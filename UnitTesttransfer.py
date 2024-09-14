
import unittest
from unittest.mock import patch, Mock
from your_module import transfer_amount  # Replace 'your_module' with the actual module name

class TestTransferAmount(unittest.TestCase):

    @patch('your_module.engine.connect')
    def test_transfer_amount_valid(self, mock_connect):
        mock_connect.return_value = Mock()
        sender = 1
        receiver = 2
        amount = 100

        transfer_amount(sender, receiver, amount)

        mock_connect.assert_called_once()
        sender_stmt = text("""
            UPDATE accounts
            SET balance = balance - :amount
            WHERE id = :sender;
        """)
        receiver_stmt = text("""
            UPDATE accounts
            SET balance = balance + :amount
            WHERE id = :receiver;
        """)
        self.assertEqual(mock_connect.return_value.execute.call_args_list, [
            [(sender_stmt, {"sender": sender, "receiver": receiver, "amount": amount})],
            [(receiver_stmt, {"sender": sender, "receiver": receiver, "amount": amount})],
        ])
        mock_connect.return_value.commit.assert_called_once()

    @patch('your_module.engine.connect')
    def test_transfer_amount_missing_table(self, mock_connect):
        mock_connect.return_value = Mock()
        sender = 1
        receiver = 2
        amount = 100

        transfer_amount(sender, receiver, amount)

        mock_connect.assert_called_once()
        mock_connect.return_value.execute.assert_called_once()
        mock_connect.return_value.commit.assert_called_once()

    @patch('your_module.engine.connect')
    def test_transfer_amountsender_non_existent(self, mock_connect):
        mock_connect.return_value = Mock()
        sender = 99
        receiver = 2
        amount = 100

        with self.assertRaises(Exception):
            transfer_amount(sender, receiver, amount)

        mock_connect.assert_called_once()
        mock_connect.return_value.execute.assert_called_once()
        mock_connect.return_value.rollback.assert_called_once()

    @patch('your_module.engine.connect')
    def test_transfer_amountreceiver_non_existent(self, mock_connect):
        mock_connect.return_value = Mock()
        sender = 1
        receiver = 99
        amount = 100

        with self.assertRaises(Exception):
            transfer_amount(sender, receiver, amount)

        mock_connect.assert_called_once()
        mock_connect.return_value.execute.assert_called_once()
        mock_connect.return_value.rollback.assert_called_once()

if __name__ == '__main__':
    unittest.main()
