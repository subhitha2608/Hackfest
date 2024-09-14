
import unittest
from unittest.mock import patch, Mock
from transfer_funds import transfer_funds

class TestTransferFunds(unittest.TestCase):

    @patch.object(engine, 'execute')
    @patch('config.engine.connect')
    def test_transfer_funds(self, mock_connect, mock_execute):
        p_sender = 123
        p_receiver = 456
        p_amount = 100
        mock_conn = Mock()
        mock_conn.commit = Mock()
        mock_connect.return_value = mock_conn
        
        sender_update_mock = Mock()
        sender_update_mock.return_value = 123
        receiver_update_mock = Mock()
        receiver_update_mock.return_value = 456
        query_mock = Mock()
        query_mock.return_value.fetchall.return_value = [(123, 23), (456, 14)]
        
        mock_execute.side_effect = [sender_update_mock, receiver_update_mock, query_mock]
        
        df = transfer_funds(p_sender, p_receiver, p_amount)
        self.assertEqual(df.shape, (2, 1))
        self.assertEqual(engine.execute.call_count, 3)
        self.assertEqual(mock_conn.commit.call_count, 2)
        self.assertEqual(sender_update_mock.call_count, 1)
        self.assertEqual(receiver_update_mock.call_count, 1)
        self.assertEqual(query_mock.call_count, 1)

    @patch.object(engine, 'execute')
    @patch('config.engine.connect')
    def test_transfer_funds_with_zero_amount(self, mock_connect, mock_execute):
        p_sender = 123
        p_receiver = 456
        p_amount = 0
        mock_conn = Mock()
        mock_conn.commit = Mock()
        mock_connect.return_value = mock_conn
        
        sender_update_mock = Mock()
        sender_update_mock.return_value = 123
        receiver_update_mock = Mock()
        receiver_update_mock.return_value = 456
        query_mock = Mock()
        query_mock.return_value.fetchall.return_value = [(123, 23), (456, 14)]
        
        mock_execute.side_effect = [sender_update_mock, receiver_update_mock, query_mock]
        
        df = transfer_funds(p_sender, p_receiver, p_amount)
        self.assertEqual(df.shape, (2, 1))
        self.assertEqual(engine.execute.call_count, 3)
        self.assertEqual(mock_conn.commit.call_count, 2)
        self.assertEqual(sender_update_mock.call_count, 1)
        self.assertEqual(receiver_update_mock.call_count, 1)
        self.assertEqual(query_mock.call_count, 1)

    @patch.object(engine, 'execute')
    @patch('config.engine.connect')
    def test_transfer_funds_with_invalid_sender(self, mock_connect, mock_execute):
        p_sender = 123
        p_receiver = 456
        p_amount = 100
        mock_conn = Mock()
        mock_conn.commit = Mock()
        mock_connect.return_value = mock_conn
        
        sender_update_mock = Mock()
        sender_update_mock.side_effect = Exception('Invalid sender')
        receiver_update_mock = Mock()
        receiver_update_mock.return_value = 456
        query_mock = Mock()
        query_mock.return_value.fetchall.return_value = [(123, 23), (456, 14)]
        
        mock_execute.side_effect = [sender_update_mock, receiver_update_mock, query_mock]
        
        with self.assertRaises(Exception):
            transfer_funds(p_sender, p_receiver, p_amount)
        self.assertEqual(engine.execute.call_count, 1)
        self.assertEqual(mock_conn.commit.call_count, 0)
        self.assertEqual(sender_update_mock.call_count, 1)
        self.assertEqual(receiver_update_mock.call_count, 0)
        self.assertEqual(query_mock.call_count, 0)

    @patch.object(engine, 'execute')
    @patch('config.engine.connect')
    def test_transfer_funds_with_invalid_receiver(self, mock_connect, mock_execute):
        p_sender = 123
        p_receiver = 456
        p_amount = 100
        mock_conn = Mock()
        mock_conn.commit = Mock()
        mock_connect.return_value = mock_conn
        
        sender_update_mock = Mock()
        sender_update_mock.return_value = 123
        receiver_update_mock = Mock()
        receiver_update_mock.side_effect = Exception('Invalid receiver')
        query_mock = Mock()
        query_mock.return_value.fetchall.return_value = [(123, 23), (456, 14)]
        
        mock_execute.side_effect = [sender_update_mock, receiver_update_mock, query_mock]
        
        with self.assertRaises(Exception):
            transfer_funds(p_sender, p_receiver, p_amount)
        self.assertEqual(engine.execute.call_count, 2)
        self.assertEqual(mock_conn.commit.call_count, 1)
        self.assertEqual(sender_update_mock.call_count, 1)
        self.assertEqual(receiver_update_mock.call_count, 1)
        self.assertEqual(query_mock.call_count, 0)

if __name__ == '__main__':
    unittest.main()
