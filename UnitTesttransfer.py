
import unittest
from unittest.mock import patch, Mock
from your_module import transfer_amount

class TestTransferAmount(unittest.TestCase):
    @patch('your_module.engine')
    @patch('your_module.text')
    def test_transfer_amount(self, mock_text, mock_engine):
        sender = 1
        receiver = 2
        amount = 10

        # Mock the engine and text functions
        mock_engine.connect.return_value = Mock()
        mock_engine.connect.return_value.execute.return_value = None
        mock_engine.connect.return_value.commit.return_value = None
        mock_engine.connect.return_value.close.return_value = None
        mock_text.return_value = "UPDATE accounts SET balance = balance - :amount WHERE id = :sender;\nUPDATE accounts SET balance = balance + :amount WHERE id = :receiver;"

        # Call the transfer_amount function
        transfer_amount(sender, receiver, amount)

        # Assert that the engine and text functions were called correctly
        mock_engine.connect.assert_called_once()
        mock_engine.connect.return_value.execute.assert_called_once_with(text=mock_text.return_value, params={'sender': sender, 'receiver': receiver, 'amount': amount})
        mock_engine.connect.return_value.commit.assert_called_once()
        mock_engine.connect.return_value.close.assert_called_once()

    def test_transfer_amount_invalid_sender(self):
        sender = 0
        receiver = 2
        amount = 10

        # Call the transfer_amount function
        with self.assertRaises(ValueError):
            transfer_amount(sender, receiver, amount)

    def test_transfer_amount_invalid_receiver(self):
        sender = 1
        receiver = 0
        amount = 10

        # Call the transfer_amount function
        with self.assertRaises(ValueError):
            transfer_amount(sender, receiver, amount)

    def test_transfer_amount_negative_amount(self):
        sender = 1
        receiver = 2
        amount = -10

        # Call the transfer_amount function
        with self.assertRaises(ValueError):
            transfer_amount(sender, receiver, amount)

    def test_transfer_amount_zero_amount(self):
        sender = 1
        receiver = 2
        amount = 0

        # Call the transfer_amount function
        transfer_amount(sender, receiver, amount)

if __name__ == '__main__':
    unittest.main()
