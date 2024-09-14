
import unittest
from your_module import transfer_funds  # import the function from your module

class TestTransferFunds(unittest.TestCase):

    def test_transfer_funds_successful(self):
        with self.assertLogs(level='INFO') as cm:
            result = transfer_funds(1, 2, 100)
            self.assertEqual(result, "Funds transfer successful.")
            self.assertEqual(len(cm.records), 1)

    def test_transfer_funds_failed_due_to_query_error(self):
        with self.assertLogs(level='ERROR') as cm:
            with unittest.mock.patch('your_module.engine.connect', side_effect=psycopg2.Error):
                result = transfer_funds(1, 2, 100)
                self.assertEqual(result, "Funds transfer failed.")
                self.assertEqual(len(cm.records), 1)

    def test_transfer_funds_failed_due_to_invalid_account_id(self):
        with self.assertLogs(level='INFO') as cm:
            result = transfer_funds(123456, 2, 100)
            self.assertEqual(result, "Funds transfer failed.")
            self.assertEqual(len(cm.records), 1)

    def test_transfer_funds_failed_due_to_negative_amount(self):
        with self.assertLogs(level='INFO') as cm:
            result = transfer_funds(1, 2, -100)
            self.assertEqual(result, "Funds transfer failed.")
            self.assertEqual(len(cm.records), 1)

    def test_transfer_funds_failed_due_to_receiving_account_with_zero_balance(self):
        with self.assertLogs(level='INFO') as cm:
            result = transfer_funds(1, 2, 1000)
            self.assertEqual(result, "Funds transfer failed.")
            self.assertEqual(len(cm.records), 1)


if __name__ == '__main__':
    unittest.main()
