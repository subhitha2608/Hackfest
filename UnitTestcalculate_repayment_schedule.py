
import unittest
from datetime import date
from loan_repayment_schedule import calculate_repayment_schedule

class TestLoanRepaymentSchedule(unittest.TestCase):

    def test_calculate_repayment_schedule_valid_loan(self):
        loan_id = 1
        loan_details = {
            'loanamount': 100000,
            'interestrate': 6,
            'loanterm': 5,
            'startdate': date(2022, 1, 1)
        }
        calculate_repayment_schedule(loan_id, **loan_details)

    def test_calculate_repayment_schedule_invalid_loan_id(self):
        loan_id = 0
        with self.assertRaises(Exception):
            calculate_repayment_schedule(loan_id)

    def test_calculate_repayment_schedule_invalid_loan_details(self):
        loan_id = 1
        loan_details = {
            'loanamount': 0,
            'interestrate': -1,
            'loanterm': 0,
            'startdate': date(2022, 1, 1)
        }
        with self.assertRaises(Exception):
            calculate_repayment_schedule(loan_id, **loan_details)

    def test_calculate_repayment_schedule_database_error(self):
        loan_id = 1
        loan_details = {
            'loanamount': 100000,
            'interestrate': 6,
            'loanterm': 5,
            'startdate': date(2022, 1, 1)
        }
        with unittest.mock.patch('loan_repayment_schedule.engine.connect') as connect:
            connect.side_effect = psycopg2.Error('test error')
            with self.assertRaises(Exception):
                calculate_repayment_schedule(loan_id, **loan_details)

    def test_calculate_repayment_schedule_rollback(self):
        loan_id = 1
        loan_details = {
            'loanamount': 100000,
            'interestrate': 6,
            'loanterm': 5,
            'startdate': date(2022, 1, 1)
        }
        with unittest.mock.patch('loan_repayment_schedule.engine.connect') as connect:
            with unittest.mock.patch('loan_repayment_schedule.conn.commit') as commit:
                connect.return_value = unittest.mock.Mock(spec=psycopg2.connect)
                commit.side_effect = psycopg2.Error('test error')
                with self.assertRaises(Exception):
                    calculate_repayment_schedule(loan_id, **loan_details)
                self.assertRaises(psycopg2.Error, commit)
                self.assertIsNotNone(connect.return_value.rollback.called)

if __name__ == '__main__':
    unittest.main()
