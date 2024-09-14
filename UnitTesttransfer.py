
import unittest
from unittest.mock import patch, Mock
from your_module import transfer_amount  # replace 'your_module' with the actual module name

class TestTransferAmount(unittest.TestCase):
    @patch('your_module.engine.connect')
    def test_transfer_amount_success(self, mock_connect):
        mock_conn = Mock()
        mock_connect.return_value = mock_conn
        mock_conn.execute.return_value = None
        mock_conn.commit.return_value = None
        mock_conn.close.return_value = None

        transfer_amount(1, 2, 10.0)

        self.assertEqual(mock_conn.execute.call_count, 2)
        mock_conn.commit.assert_called_once()
        mock_conn.close.assert_called_once()

    @patch('your_module.engine.connect')
    def test_transfer_amount_sender_update_failure(self, mock_connect):
        mock_conn = Mock()
        mock_connect.return_value = mock_conn
        mock_conn.execute.side_effect = [None, psycopg2.Error('Error updating sender')]

        with self.assertRaises(psycopg2.Error):
            transfer_amount(1, 2, 10.0)

        self.assertEqual(mock_conn.execute.call_count, 2)
        mock_conn.rollback.assert_called_once()
        mock_conn.close.assert_called_once()

    @patch('your_module.engine.connect')
    def test_transfer_amount_receiver_update_failure(self, mock_connect):
        mock_conn = Mock()
        mock_connect.return_value = mock_conn
        mock_conn.execute.side_effect = [psycopg2.Error('Error updating sender'), None]

        with self.assertRaises(psycopg2.Error):
            transfer_amount(1, 2, 10.0)

        self.assertEqual(mock_conn.execute.call_count, 2)
        mock_conn.rollback.assert_called_once()
        mock_conn.close.assert_called_once()

    @patch('your_module.engine.connect')
    def test_transfer_amount_invalid_sender(self, mock_connect):
        with self.assertRaises(TypeError):
            transfer_amount(None, 2, 10.0)

    @patch('your_module.engine.connect')
    def test_transfer_amount_invalid_receiver(self, mock_connect):
        with self.assertRaises(TypeError):
            transfer_amount(1, None, 10.0)

    @patch('your_module.engine.connect')
    def test_transfer_amount_invalid_amount(self, mock_connect):
        with self.assertRaises(TypeError):
            transfer_amount(1, 2, 'ten')

if __name__ == '__main__':
    unittest.main()
