
import unittest
from unittest.mock import patch, Mock
from sqlalchemy.engine import Engine
from sqlalchemy.exc import DBAPIError
from psycopg2 import Error
from your_module import calculate_repayment_schedule

class TestCalculateRepaymentSchedule(unittest.TestCase):

    @patch('your_module.engine')
    def test_calculate_repayment_schedule_success(self, engine_mock):
        engine_mock.execute.return_value.fetchone.return_value = (10000, 5, 60, '2022-01-01')
        engine_mock.execute.return_value = Mock()
        self.assertEqual(calculate_repayment_schedule(1), "Repayment schedule calculated successfully")
        engine_mock.execute.assert_called()

    @patch('your_module.engine')
    def test_calculate_repayment_schedule_dbapi_error(self, engine_mock):
        engine_mock.execute.side_effect = DBAPIError(None, None, None)
        with self.assertRaises(DBAPIError):
            calculate_repayment_schedule(1)

    @patch('your_module.engine')
    def test_calculate_repayment_schedule_psycopg2_error(self, engine_mock):
        engine_mock.execute.side_effect = Error()
        with self.assertRaises(Error):
            calculate_repayment_schedule(1)

    @patch('your_module.engine')
    def test_calculate_repayment_schedule_loan_id_none(self, engine_mock):
        with self.assertRaises(TypeError):
            calculate_repayment_schedule(None)

    @patch('your_module.engine')
    def test_calculate_repayment_schedule_loan_id_string(self, engine_mock):
        with self.assertRaises(TypeError):
            calculate_repayment_schedule('1')

    @patch('your_module.engine')
    def test_calculate_repayment_schedule_loan_id_negative(self, engine_mock):
        with self.assertRaises(ValueError):
            calculate_repayment_schedule(-1)

if __name__ == '__main__':
    unittest.main()
