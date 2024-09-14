
import unittest
from unittest.mock import patch, Mock
from your_module import transfer_funds
import psycopg2

class TestTransferFunds(unittest.TestCase):

    @patch('your_module.engine')
    def test_transfer_funds_success(self, mock_engine):
        mock_connection = Mock()
        mock_engine.connect.return_value = mock_connection
        transfer_funds(1, 2, 100)
        mock_connection.execute.assert_called()
        mock_connection.commit.assert_called()
        mock_connection.close.assert_called()

    @patch('your_module.engine')
    def test_transfer_funds_psycopg2_error(self, mock_engine):
        mock_connection = Mock()
        mock_connection.execute.side_effect = psycopg2.Error
        mock_engine.connect.return_value = mock_connection
        with self.assertRaises(psycopg2.Error):
            transfer_funds(1, 2, 100)
        mock_connection.rollback.assert_called()
        mock_connection.close.assert_called()

    @patch('your_module.engine')
    def test_transfer_funds_zero_amount(self, mock_engine):
        mock_connection = Mock()
        mock_engine.connect.return_value = mock_connection
        transfer_funds(1, 2, 0)
        mock_connection.execute.assert_called()
        mock_connection.commit.assert_called()
        mock_connection.close.assert_called()

    @patch('your_module.engine')
    def test_transfer_funds_negative_amount(self, mock_engine):
        mock_connection = Mock()
        mock_engine.connect.return_value = mock_connection
        with self.assertRaises(ValueError):
            transfer_funds(1, 2, -100)
        mock_connection.close.assert_called()

    @patch('your_module.engine')
    def test_transfer_funds_same_sender_receiver(self, mock_engine):
        mock_connection = Mock()
        mock_engine.connect.return_value = mock_connection
        with self.assertRaises(ValueError):
            transfer_funds(1, 1, 100)
        mock_connection.close.assert_called()

if __name__ == '__main__':
    unittest.main()
