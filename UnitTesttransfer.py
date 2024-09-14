
import unittest
from unittest.mock import patch, MagicMock
from your_module import transfer_funds

class TestTransferFunds(unittest.TestCase):
    @patch('your_module.engine')
    def test_transfer_funds_success(self, mock_engine):
        mock_engine.connect = MagicMock(return_value=MagicMock(spec=['execute', 'commit', 'rollback', 'close']))
        mock_connection = mock_engine.connect.return_value
        mock_connection.execute.side_effect = [[{'balance': 100}], [{'balance': 200}]]

        result = transfer_funds(1, 2, 50)
        self.assertEqual(result, [{'balance': 50}, {'balance': 250}])

        mock_engine.connect.assert_called_once()
        mock_connection.execute.assert_any_call(text("UPDATE accounts SET balance = balance - :amount WHERE id = :sender"), {'amount': 50, 'sender': 1})
        mock_connection.execute.assert_any_call(text("UPDATE accounts SET balance = balance + :amount WHERE id = :receiver"), {'amount': 50, 'receiver': 2})
        mock_connection.commit.assert_called_once()
        mock_connection.close.assert_called_once()

    @patch('your_module.engine')
    def test_transfer_funds_insufficient_funds(self, mock_engine):
        mock_engine.connect = MagicMock(return_value=MagicMock(spec=['execute', 'commit', 'rollback', 'close']))
        mock_connection = mock_engine.connect.return_value
        mock_connection.execute.side_effect = [[{'balance': 10}], [{'balance': 200}]]

        with self.assertRaises(Exception):
            transfer_funds(1, 2, 50)

        mock_engine.connect.assert_called_once()
        mock_connection.execute.assert_any_call(text("UPDATE accounts SET balance = balance - :amount WHERE id = :sender"), {'amount': 50, 'sender': 1})
        mock_connection.rollback.assert_called_once()
        mock_connection.close.assert_called_once()

    @patch('your_module.engine')
    def test_transfer_funds_receiver_not_found(self, mock_engine):
        mock_engine.connect = MagicMock(return_value=MagicMock(spec=['execute', 'commit', 'rollback', 'close']))
        mock_connection = mock_engine.connect.return_value
        mock_connection.execute.side_effect = [[{'balance': 100}], []]

        with self.assertRaises(Exception):
            transfer_funds(1, 2, 50)

        mock_engine.connect.assert_called_once()
        mock_connection.execute.assert_any_call(text("UPDATE accounts SET balance = balance - :amount WHERE id = :sender"), {'amount': 50, 'sender': 1})
        mock_connection.rollback.assert_called_once()
        mock_connection.close.assert_called_once()

    @patch('your_module.engine')
    def test_transfer_funds_sender_not_found(self, mock_engine):
        mock_engine.connect = MagicMock(return_value=MagicMock(spec=['execute', 'commit', 'rollback', 'close']))
        mock_connection = mock_engine.connect.return_value
        mock_connection.execute.side_effect = [[], [{'balance': 200}]]

        with self.assertRaises(Exception):
            transfer_funds(1, 2, 50)

        mock_engine.connect.assert_called_once()
        mock_connection.rollback.assert_called_once()
        mock_connection.close.assert_called_once()

if __name__ == '__main__':
    unittest.main()
