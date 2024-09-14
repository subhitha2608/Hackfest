
import unittest
from unittest.mock import patch
from your_module import transfer_money

class TestTransferMoney(unittest.TestCase):
    
    @patch('config.engine')
    def test_invalid_sender_id(self, mock_engine):
        with self.assertRaises(ValueError):
            transfer_money(0, 1, 100)

    @patch('config.engine')
    def test_invalid_receiver_id(self, mock_engine):
        with self.assertRaises(ValueError):
            transfer_money(1, 0, 100)

    @patch('config.engine')
    def test_insufficient_balance_sender(self, mock_engine):
        mock_engine.connect().execute.return_value.fetchall.return_value = [(100,)]
        with self.assertRaises(ValueError):
            transfer_money(1, 2, 150)

    @patch('config.engine')
    def test_successful_transfer(self, mock_engine):
        mock_engine.connect().execute.return_value.fetchall.return_value = [(100,)]
        transfer_money(1, 2, 50)

    @patch('config.engine')
    def test_edge_case_zero_amount(self, mock_engine):
        mock_engine.connect().execute.return_value.fetchall.return_value = [(100,)]
        transfer_money(1, 2, 0)

    @patch('config.engine')
    def test_edge_case_negative_amount(self, mock_engine):
        mock_engine.connect().execute.return_value.fetchall.return_value = [(100,)]
        transfer_money(1, 2, -50)

if __name__ == '__main__':
    unittest.main()
