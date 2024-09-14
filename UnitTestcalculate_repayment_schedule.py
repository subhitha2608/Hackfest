
import unittest
from unittest.mock import patch
from your_module import create_repayment_schedule  # replace with the actual module name

class TestRepaymentSchedule(unittest.TestCase):
    @patch('your_module.engine')
    @patch('your_module.conn')
    def test_create_repayment_schedule(self, mock_conn, mock_engine):
        loan_id = 123
        loan_amount = 10000
        interest_rate = 12
        loan_term = 60
        start_date = '2022-01-01'

        def simulate_query.Result.__getitem__(self, index):
            if index == 0:
                return loan_amount
            elif index == 1:
                return interest_rate
            elif index == 2:
                return loan_term
            elif index == 3:
                return start_date

        mock_result = MockResult(return_value=[loan_amount, interest_rate, loan_term, start_date])
        mock_engine.return_value.connect.return_value = mock_conn
        mock_conn.execute.return_value = mock_result

        create_repayment_schedule(loan_id)

        self.assertEqual(mock_conn.execute.call_count, 2)
        self.assertEqual(mock_conn.commit.call_count, 1)

    @patch('your_module.engine')
    @patch('your_module.conn')
    def test_create_repayment_schedule_error(self, mock_conn, mock_engine):
        loan_id = 123
        error = 'Database error'

        mock_engine.return_value.connect.return_value = mock_conn
        mock_conn.execute.side_effect = Exception(error)

        with self.assertRaises(Exception) as cm:
            create_repayment_schedule(loan_id)
        self.assertEqual(str(cm.exception), error)

    @patch('your_module.engine')
    @patch('your_module.conn')
    def test_create_repayment_schedule_empty_result(self, mock_conn, mock_engine):
        loan_id = 123
        result = []

        mock_engine.return_value.connect.return_value = mock_conn
        mock_conn.execute.return_value = result

        with self.assertRaises(IndexError) as cm:
            create_repayment_schedule(loan_id)
        self.assertEqual(str(cm.exception), 'list index out of range')

    @patch('your_module.engine')
    @patch('your_module.conn')
    def test_create_repayment_schedule_multiple_loans(self, mock_conn, mock_engine):
        loan_id = 123
        loan_amount = 10000
        interest_rate = 12
        loan_term = 60
        start_date = '2022-01-01'

        def simulate_query(Result.__getitem__, self, index):
            if index == 0:
                return loan_amount
            elif index == 1:
                return interest_rate
            elif index == 2:
                return loan_term
            elif index == 3:
                return start_date

        mock_result = MockResult(return_value=[loan_amount, interest_rate, loan_term, start_date])
        mock_engine.return_value.connect.return_value = mock_conn
        mock_conn.execute.return_value = [mock_result, mock_result]

        create_repayment_schedule(loan_id)

        self.assertEqual(mock_conn.execute.call_count, 4)
        self.assertEqual(mock_conn.commit.call_count, 1)

class MockResult:
    def __init__(self, return_value):
        self.return_value = return_value

    def fetchone(self):
        return self.return_value

    def __getitem__(self, index):
        return self.return_value[index]

if __name__ == '__main__':
    unittest.main()
