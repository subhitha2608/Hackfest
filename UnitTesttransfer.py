
import unittest
from your_module import transfer_amount  # Replace with your module name
from unittest.mock import patch, Mock
from your_config import engine  # Replace with your config module

class TestTransferAmount(unittest.TestCase):

    @patch('your_config.engine.execute')
    @patch('psycopg2.connect')
    def test_transfer_amount_success(self, mock_connect, mock_execute):
        # Set up mocked database connections and results
        mock_connect.return_value = Mock()
        mock_connect().execute.return_value = [Mock(balance=100)]
        mock_connect().execute.return_value = [Mock(balance=100)]

        # Call the transfer_amount function
        result = transfer_amount(sender_id=1, receiver_id=2, amount=50)

        # Check the results
        self.assertEqual(result, [(1, 50, 50), (2, 50, 100)])

    @patch('your_config.engine.execute')
    @patch('psycopg2.connect')
    def test_transfer_amount_sender_account_not_found(self, mock_connect, mock_execute):
        # Set up mocked database connections and results
        mock_connect.return_value = Mock()
        mock_connect().execute.side_effect = [None, [Mock(balance=100)]]
        mock_execute.side_effect = [None, None, None]

        # Call the transfer_amount function
        with self.assertRaises(psycopg2.Error):
            transfer_amount(sender_id=1, receiver_id=2, amount=50)

    @patch('your_config.engine.execute')
    @patch('psycopg2.connect')
    def test_transfer_amount_receiver_account_not_found(self, mock_connect, mock_execute):
        # Set up mocked database connections and results
        mock_connect.return_value = Mock()
        mock_connect().execute.side_effect = [[Mock(balance=100)], None]
        mock_execute.side_effect = [None, None, None]

        # Call the transfer_amount function
        with self.assertRaises(psycopg2.Error):
            transfer_amount(sender_id=1, receiver_id=2, amount=50)

    @patch('your_config.engine.execute')
    @patch('psycopg2.connect')
    def test_transfer_amount_amount_zero(self, mock_connect, mock_execute):
        # Set up mocked database connections and results
        mock_connect.return_value = Mock()
        mock_connect().execute.side_effect = [[Mock(balance=100)], [Mock(balance=100)]]
        mock_execute.side_effect = [None, None, None]

        # Call the transfer_amount function
        result = transfer_amount(sender_id=1, receiver_id=2, amount=0)
        self.assertEqual(result, [(1, 0, 100), (2, 0, 100)])

    @patch('your_config.engine.execute')
    @patch('psycopg2.connect')
    def test_transfer_amount_max_value_error(self, mock_connect, mock_execute):
        # Set up mocked database connections and results
        mock_connect.return_value = Mock()
        mock_connect().execute.side_effect = [[Mock(balance=2147483647)], [Mock(balance=2147483647)]]
        mock_execute.side_effect = [None, None, None]

        # Call the transfer_amount function
        with self.assertRaises(psycopg2.Error):
            transfer_amount(sender_id=1, receiver_id=2, amount=1)

    @patch('config.engine')
    @patch('psycopg2.connect')
    def test_transfer_amount_config_error(self, mock_connect, mock_engine):
        # Set up mocked database connections and results
        mock_connect.return_value = Mock()
        mock_connect().execute.side_effect = [None, None, None]
        mock_engine.execute.side_effect = psycopg2.Error('Test error')

        # Call the transfer_amount function
        with self.assertRaises(psycopg2.Error):
            transfer_amount(sender_id=1, receiver_id=2, amount=50)
