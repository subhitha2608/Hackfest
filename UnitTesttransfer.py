
import unittest
from unit_tests.test_transfer import transfer  # Import the function to be tested

class TestTransferFunction(unittest.TestCase):
    def setUp(self):
        # Set up test data
        self.sender_id = 1
        self.receiver_id = 2
        self.amount = 10.0

    def test_transfer_valid(self):
        sender_balance, receiver_balance = transfer(self.sender_id, self.receiver_id, self.amount)
        self.assertEqual(sender_balance[1], self.amount)
        self.assertEqual(receiver_balance[1], self.amount)
        # Verify the balance of the sender account has decreased
        self.assertEqual(round(sender_balance[1], 2), self.amount)
        # Verify the balance of the receiver account has increased
        self.assertEqual(round(receiver_balance[1], 2), self.amount)

    def test_transfer_zero_amount(self):
        sender_balance, receiver_balance = transfer(self.sender_id, self.receiver_id, 0)
        self.assertEqual(sender_balance[1], sender_balance[1])
        self.assertEqual(receiver_balance[1], receiver_balance[1])

    def test_transfer_invalid_sender_id(self):
        with self.assertRaises(sqlalchemy.exc.IntegrityError):
            transfer(0, self.receiver_id, self.amount)

    def test_transfer_invalid_receiver_id(self):
        with self.assertRaises(sqlalchemy.exc.IntegrityError):
            transfer(self.sender_id, 0, self.amount)

    def test_transfer_invalid_amount_type(self):
        with self.assertRaises(TypeError):
            transfer(self.sender_id, self.receiver_id, 'abc')

    def tearDown(self):
        # Clean up test data
        pass

if __name__ == '__main__':
    unittest.main()
