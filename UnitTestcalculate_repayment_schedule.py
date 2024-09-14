
import unittest
from unittest.mock import Mock
from your_module import calculate_repayment_schedule  # replace with the actual module name

class TestCalculateRepaymentSchedule(unittest.TestCase):

    def setUp(self):
        self.engine = Mock()
        self.engine.connect.return_value = Mock()
        self.conn = self.engine.connect.return_value
        self.conn.execute.return_value = Mock()
        self.conn.execute.return_value.fetchall.return_value = [(1000, 5, 60, '2020-01-01')]
        self.engine.connect.return_value.commit.return_value = None
        self.engine.connect.return_value.rollback.return_value = None
        self.conn.close.return_value = None

    def test_calculate_repayment_schedule_valid_loan_id(self):
        result = calculate_repayment_schedule(1)
        self.conn.execute.assert_called_once()
        self.conn.execute().return_value.fetchone.assert_called_once()
        self.conn.execute().return_value.fetchall.assert_called_once()
        self.assertEqual(len(result), len([(1000, 5, 60, '2020-01-01')]))

    def test_calculate_repayment_schedule_invalid_loan_id(self):
        self.conn.execute().return_value.fetchone.return_value = None
        result = calculate_repayment_schedule(1)
        self.conn.execute.assert_called_once()
        self.conn.execute().return_value.fetchone.assert_called_once()
        self.assertEqual(result, [])

    def test_calculate_repayment_schedule_error_occurs(self):
        self.conn.execute().return_value.fetchone.side_effect = psycopg2.Error('Error')
        result = calculate_repayment_schedule(1)
        self.conn.execute.assert_called_once()
        self.conn.execute().return_value.fetchone.assert_called_once()
        self.assertEqual(result, [])

    def test_calculate_repayment_schedule_cursor_error_occurs(self):
        self.conn.execute.side_effect = Exception('Cursor error')
        result = calculate_repayment_schedule(1)
        self.conn.execute.assert_called_once()
        self.assertEqual(result, [])

    def test_calculate_repayment_schedule_repayment_schedule(self):
        result = calculate_repayment_schedule(1)
        self.assertEqual(len(result[0]), 8)
        self.assertEqual(result[0][0], 1)
        self.assertEqual(result[0][1], 1000)
        self.assertEqual(result[0][2], 0)
        self.assertEqual(result[0][3], 0)
        self.assertEqual(result[0][4], 50)
        self.assertEqual(result[0][5], 30)
        self.assertEqual(result[0][6], 900)

if __name__ == '__main__':
    unittest.main()
