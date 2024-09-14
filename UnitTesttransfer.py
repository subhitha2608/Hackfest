
import unittest
from unittest.mock import patch, Mock
from your_module import transfer_amount  # Replace 'your_module' with the actual module name

class TestTransferAmount(unittest.TestCase):

    def setUp(self):
        self.p_sender = 1
        self.p_receiver = 2
        self.p_amount = 100

    @patch('your_module.engine')
    @patch('your_module.sqlalchemy')
    @patch('your_module.conn')
    @patch('your_module.conn.commit')
    @patch('your_module.engine.connect')
    def test_transfer_amount_success(self, mock_engine_connect, mock_conn_commit, mock_conn, mock_sqlalchemy, mock_engine):
        result_sender = Mock()
        result_receiver = Mock()
        result_balances = Mock()
        mock_sqlalchemy.text.return_value = Mock()
        mock_sqlalchemy.text.return_value = Mock()
        mock_engine.execute.return_value = result_sender
        mock_engine.connect.return_value = conn = Mock()
        conn.commit.return_value = None
        result_balances = [(1, 100), (2, 200)]
        mock_engine.execute.return_value = result_balances

        self.assertEqual(transfer_amount(self.p_sender, self.p_receiver, self.p_amount), result_balances)

    @patch('your_module.engine')
    @patch('your_module.sqlalchemy')
    @patch('your_module.conn')
    @patch('your_module.conn.commit')
    @patch('your_module.engine.connect')
    def test_transfer_amount_sender_does_not_exist(self, mock_engine_connect, mock_conn_commit, mock_conn, mock_sqlalchemy, mock_engine):
        mock_engine.execute.side_effect = Exception("Error")
        self.assertIsNone(transfer_amount(self.p_sender, self.p_receiver, self.p_amount))

    @patch('your_module.engine')
    @patch('your_module.sqlalchemy')
    @patch('your_module.conn')
    @patch('your_module.conn.commit')
    @patch('your_module.engine.connect')
    def test_transfer_amount_receiver_does_not_exist(self, mock_engine_connect, mock_conn_commit, mock_conn, mock_sqlalchemy, mock_engine):
        mock_engine.execute.side_effect = Exception("Error")
        self.assertIsNone(transfer_amount(self.p_sender, self.p_receiver, self.p_amount))

    @patch('your_module.engine')
    @patch('your_module.sqlalchemy')
    @patch('your_module.conn')
    @patch('your_module.conn.commit')
    @patch('your_module.engine.connect')
    def test_transfer_amount_invalid_amount(self, mock_engine_connect, mock_conn_commit, mock_conn, mock_sqlalchemy, mock_engine):
        self.p_amount = "Invalid amount"
        mock_engine.execute.side_effect = Exception("Error")
        self.assertIsNone(transfer_amount(self.p_sender, self.p_receiver, self.p_amount))

    @patch('your_module.engine')
    @patch('your_module.sqlalchemy')
    @patch('your_module.conn')
    @patch('your_module.conn.commit')
    @patch('your_module.engine.connect')
    def test_transfer_amount_error_in_query(self, mock_engine_connect, mock_conn_commit, mock_conn, mock_sqlalchemy, mock_engine):
        mock_engine.execute.side_effect = Exception("Error")
        self.assertIsNone(transfer_amount(self.p_sender, self.p_receiver, self.p_amount))

if __name__ == '__main__':
    unittest.main()
