
import unittest
from unittest.mock import patch, Mock
from your_module import transfer_amount  # Replace with the actual module name

class TestTransferAmount(unittest.TestCase):
    @patch.object(psycopg2, 'connect')
    @patch.object(pd, 'read_sql')
    @patch('config.engine')
    def test_transfer_amount(self, mock_engine, mock_read_sql, mock_connect):
        mock_connect.return_value = Mock()
        mock_engine.connect.return_value = mock_connect
        mock_read_sql.return_value = pd.DataFrame({'id': [1], 'balance': [100]})

        transfer_amount(1, 2, 50)

        self.assertEqual(mock_connect().execute.call_count, 2)
        self.assertEqual(mock_connect().commit.call_count, 2)
        self.assertEqual(mock_connect().close.call_count, 1)

    @patch.object(psycopg2, 'connect')
    @patch.object(pd, 'read_sql')
    @patch('config.engine')
    def test_transfer_amount_invalid_sender(self, mock_engine, mock_read_sql, mock_connect):
        mock_connect.return_value = Mock()
        mock_engine.connect.return_value = mock_connect
        mock_read_sql.return_value = pd.DataFrame({'id': [1], 'balance': [100]}).set_index('id')

        with self.assertRaises(SequrityError):
            transfer_amount(3, 2, 50)

    @patch.object(psycopg2, 'connect')
    @patch.object(pd, 'read_sql')
    @patch('config.engine')
    def test_transfer_amount_invalid_receiver(self, mock_engine, mock_read_sql, mock_connect):
        mock_connect.return_value = Mock()
        mock_engine.connect.return_value = mock_connect
        mock_read_sql.return_value = pd.DataFrame({'id': [1], 'balance': [100]}).set_index('id')

        with self.assertRaises(SequrityError):
            transfer_amount(1, 3, 50)

    @patch.object(psycopg2, 'connect')
    @patch.object(pd, 'read_sql')
    @patch('config.engine')
    def test_transfer_amount_incorrect_amount(self, mock_engine, mock_read_sql, mock_connect):
        mock_connect.return_value = Mock()
        mock_engine.connect.return_value = mock_connect
        mock_read_sql.return_value = pd.DataFrame({'id': [1], 'balance': [100]}).set_index('id')

        with self.assertRaises(SequrityError):
            transfer_amount(1, 2, 150)

if __name__ == '__main__':
    unittest.main()
