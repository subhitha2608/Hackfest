
import unittest
from unittest.mock import patch, mock_open
from your_module import transfer_amount

class TestTransferAmount(unittest.TestCase):

    @patch('your_module.engine.execute')
    def test_transfer_amount_success(self, execute):
        execute.side_effect = [None, None, None]  # SUCCESS, SUCCESS, COMMIT
        self.assertEqual(transfer_amount(1, 2, 10), "Amount transferred successfully")

    @patch('your_module.engine.execute')
    def test_transfer_amount_error_psycopg2(self, execute):
        exc = Exception("Test psycopg2 error")
        execute.side_effect = [None, None, exc]  # SUCCESS, SUCCESS, ROLLBACK
        self.assertEqual(transfer_amount(1, 2, 10), str(exc))

    @patch('your_module.engine.execute')
    def test_transfer_amount_error_integrity(self, execute):
        exc = exc.IntegrityError("Test integrity error")
        execute.side_effect = [None, exc, None]  # SUCCESS, ROLLBACK, COMMIT
        self.assertEqual(transfer_amount(1, 2, 10), str(exc))

    @patch('your_module.engine.execute')
    def test_transfer_amount_error_other(self, execute):
        exc = Exception("Test other error")
        execute.side_effect = [None, exc, None]  # SUCCESS, ROLLBACK, COMMIT
        self.assertEqual(transfer_amount(1, 2, 10), str(exc))

    @patch('your_module.engine.execute')
    def test_transfer_amount_sender_error(self, execute):
        sender_update = text("UPDATE accounts SET balance = balance - :p_amount")
        sender_update_mock = mock_open(read_data=sender_update)
        with patch('builtins.open', sender_update_mock):
            execute.side_effect = [None, Exception("Test sender error"), None]
            self.assertEqual(transfer_amount(1, 2, 10), str("Test sender error"))

    @patch('your_module.engine.execute')
    def test_transfer_amount_receiver_error(self, execute):
        receiver_update = text("UPDATE accounts SET balance = balance + :p_amount")
        receiver_update_mock = mock_open(read_data=receiver_update)
        with patch('builtins.open', receiver_update_mock):
            execute.side_effect = [None, None, Exception("Test receiver error")]
            self.assertEqual(transfer_amount(1, 2, 10), str("Test receiver error"))

if __name__ == '__main__':
    unittest.main()
