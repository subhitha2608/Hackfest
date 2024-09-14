
import unittest
from unittest.mock import patch, Mock
from your_module import calculate_repayment_schedule

class TestCalculateRepaymentSchedule(unittest.TestCase):

    @patch('your_module.engine.execute.return_value.fetchone.return_value')
    def test LoanDetails(self, result_mock):
        result_mock.return_value = (1000000, 5, 360, '2020-01-01')
        calculate_repayment_schedule(1)
        self.assertEqual(calculate_repayment_schedule.mes, 10)

    @patch('your_module.engine.execute')
    @patch('your_module.engine.commit')
    def test_RepaymentSchedule(self, commit_mock, execute_mock):
        execute_mock.return_value = Mock()
        execute_mock.return_value.__enter__.return_value.fetchall.return_value = None
        calculate_repayment_schedule(1)
        execute_mock.assert_called()
        commit_mock.assert_called()

    @patch('your_module.engine.execute')
    @patch('your_module.engine.commit')
    @patch('your_module.engine.execute.side_effect')
    def test_RepaymentScheduleMultipleCalls(self, execute_mock_side_effect, commit_mock, execute_mock):
        loan_id = 1
        calculate_repayment_schedule(loan_id)
        execute_mock.assert_called_once()
        commit_mock.assert_called_once()

    @patch('your_module.engine.execute')
    @patch('your_module.engine.commit')
    @patch('your_module.engine.execute.side_effect')
    def test_RepaymentScheduleOneCall(self, execute_mock_side_effect, commit_mock, execute_mock):
        loan_id = 1
        calculate_repayment_schedule(loan_id)
        execute_mock.assert_called_once()
        commit_mock.assert_called_once()

    @patch('your_module.engine.execute')
    @patch('your_module.engine.commit')
    @patch('your_module.engine.execute.side_effect')
    def test_RepaymentScheduleMultipleCalls(self, execute_mock_side_effect, commit_mock, execute_mock):
        calculate_repayment_schedule(1)
        execute_mock.assert_called_once()
        commit_mock.assert_called_once()

    @patch('your_module.engine.execute')
    @patch('your_module.engine.commit')
    @patch('your_module.engine.execute.side_effect')
    def test_CloseDBConnection(self, side_effect, commit_mock, execute_mock):
        loan_id = 1
        calculate_repayment_schedule(loan_id)
        execute_mock.assert_called_once()
        commit_mock.assert_called_once()

if __name__ == '__main__':
    unittest.main()
